#!/usr/bin/env python3
"""
Axiom Audit Checker for Syracuse Formalization (MIN-85 / PRD-27)

Verifies:
1. All 54 formalized theorems in Collatz/Syracuse.lean are accounted for.
2. Zero `sorry`, zero `admit`, zero `unsafe`, zero custom `axiom` declarations across ALL Lean files.
3. Strict fail-closed Lake kernel build: executes `lake build` to confirm kernel acceptance.
4. Strict allowlist validation of Lean 4 `#print axioms` output:
   Only foundational axioms {"propext", "Classical.choice", "Quot.sound"} are permitted.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

EXPECTED_THEOREMS = [
    # Section 1: Valuations
    "v2_zero",
    "v2_two",
    "v2_four",
    "v2_eight",
    "v2_sixteen",
    # Section 2: Fixed Point and Elementary Orbits
    "syracuse_one",
    "syracuse_three",
    "syracuse_five",
    "syracuse_two_steps_three",
    "descent_three",
    # Section 3: Deep Orbits (7, 9, 15)
    "syracuse_seven",
    "syracuse_eleven",
    "syracuse_seventeen",
    "syracuse_thirteen",
    "descent_seven",
    "syracuse_nine",
    "descent_nine",
    "syracuse_fifteen",
    "syracuse_twentythree",
    "syracuse_thirtyfive",
    "syracuse_fiftythree",
    "descent_fifteen",
    # Section 4: Odd Orbits (19, 21, 25, 27)
    "syracuse_nineteen",
    "syracuse_twentynine",
    "descent_nineteen",
    "syracuse_twentyone",
    "descent_twentyone",
    "syracuse_twentyfive",
    "descent_twentyfive",
    "syracuse_twentyseven_step1",
    "syracuse_fortyone",
    # Section 5: Certificate Soundness & LEMMA_TARGET Realization
    "certificate_sound",
    "batch_sound",
    "has_descent_three",
    "has_descent_five",
    "has_descent_seven",
    "has_descent_nine",
    "has_descent_eleven",
    "has_descent_thirteen",
    "has_descent_fifteen",
    "has_descent_seventeen",
    "has_descent_nineteen",
    "has_descent_twentyone",
    "has_descent_twentythree",
    "has_descent_twentyfive",
    "has_descent_twentyseven",
    "has_descent_twentynine",
    "has_descent_thirtyone",
    "descent_cert_three",
    "descent_cert_seven",
    "descent_cert_fifteen",
    "descent_cert_twentyseven",
    "canonical_batch_valid",
    "canonical_batch_sound",
]

ALLOWED_FOUNDATIONAL_AXIOMS = {
    "propext",
    "Classical.choice",
    "Quot.sound",
}

def strip_lean_comments_and_strings(code: str) -> str:
    """Strip comments and string literals from Lean code to inspect declarations."""
    # Remove block comments
    code = re.sub(r"/-\!?(.*?)-/", "", code, flags=re.DOTALL)
    # Remove string literals
    code = re.sub(r'"([^"\\]|\\.)*"', '""', code)
    # Remove line comments
    lines = [re.sub(r"--.*$", "", line) for line in code.splitlines()]
    return "\n".join(lines)

def audit_source_files(base_dir: Path) -> dict:
    lean_files = list(base_dir.rglob("*.lean"))
    if not lean_files:
        raise FileNotFoundError(f"No .lean files found in {base_dir}")

    syracuse_lean = base_dir / "Collatz" / "Syracuse.lean"
    audit_lean = base_dir / "AxiomAudit.lean"
    if not syracuse_lean.exists():
        raise FileNotFoundError(f"Missing {syracuse_lean}")
    if not audit_lean.exists():
        raise FileNotFoundError(f"Missing {audit_lean}")

    forbidden_patterns = [
        ("sorry", re.compile(r"\bsorry\b")),
        ("admit", re.compile(r"\badmit\b")),
        ("unsafe", re.compile(r"\bunsafe\b")),
        ("axiom", re.compile(r"\baxiom\s+")),
    ]
    scanned_files = []

    for fpath in sorted(lean_files):
        content = fpath.read_text(encoding="utf-8")
        clean_content = strip_lean_comments_and_strings(content)
        scanned_files.append(str(fpath.relative_to(base_dir)))
        for word, pat in forbidden_patterns:
            for line_no, line in enumerate(clean_content.splitlines(), start=1):
                if pat.search(line):
                    raise ValueError(
                        f"Found forbidden keyword '{word}' in {fpath.name}:{line_no}: {line.strip()}"
                    )

    # Verify all expected theorems exist in Syracuse.lean
    syracuse_content = syracuse_lean.read_text(encoding="utf-8")
    clean_syracuse = strip_lean_comments_and_strings(syracuse_content)
    thms = re.findall(r"theorem\s+([A-Za-z0-9_]+)", clean_syracuse)
    missing = [t for t in EXPECTED_THEOREMS if t not in thms]
    if missing:
        raise ValueError(f"Missing expected theorems in {syracuse_lean}: {missing}")

    return {
        "status": "PASS",
        "scanned_files_count": len(scanned_files),
        "scanned_files": scanned_files,
        "theorem_count": len(thms),
        "theorems": thms,
        "forbidden_audit": "CLEAN",
    }

def find_lake_binary() -> str:
    """Locate lake binary in PATH or standard elan / homebrew paths."""
    lake = shutil.which("lake")
    if lake:
        return lake

    candidates = [
        Path.home() / ".elan" / "bin" / "lake",
        Path("/opt/homebrew/bin/lake"),
        Path("/usr/local/bin/lake"),
        Path("/usr/bin/lake"),
    ]
    for c in candidates:
        if c.is_file() and os.access(c, os.X_OK):
            return str(c)
    return ""

def parse_axiom_audit_output(output: str) -> dict:
    """
    Strictly parse '#print axioms <name>' output and enforce allowlist.
    Matches lines like:
      'Collatz.v2_zero' does not depend on any axioms
      'Collatz.thm' depends on axioms: [propext, Classical.choice]
    """
    pattern = re.compile(
        r"'([A-Za-z0-9_\.]+)'\s+(does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])"
    )
    checked_theorems = {}

    for line in output.splitlines():
        line = line.strip()
        match = pattern.search(line)
        if match:
            full_name = match.group(1)
            thm_name = full_name.split(".")[-1]
            kind = match.group(2)
            if "does not depend on any axioms" in kind:
                axioms = set()
            else:
                raw_axioms = match.group(3)
                axioms = {ax.strip() for ax in raw_axioms.split(",") if ax.strip()}

            disallowed = axioms - ALLOWED_FOUNDATIONAL_AXIOMS
            if disallowed:
                raise ValueError(
                    f"Theorem '{full_name}' depends on non-whitelisted/custom axioms: {disallowed}"
                )
            checked_theorems[thm_name] = axioms

    return checked_theorems

def run_lake_audit(base_dir: Path) -> dict:
    lake_bin = find_lake_binary()
    if not lake_bin:
        return {
            "status": "FAIL",
            "error": (
                "Lake executable not found in PATH or standard elan directories. "
                "Kernel verification is mandatory (fail-closed)."
            ),
        }

    env = os.environ.copy()
    lake_dir = str(Path(lake_bin).parent)
    if lake_dir not in env.get("PATH", ""):
        env["PATH"] = f"{lake_dir}:{env.get('PATH', '')}"

    try:
        proc = subprocess.run(
            [lake_bin, "build"],
            cwd=base_dir,
            capture_output=True,
            text=True,
            timeout=120,
            env=env,
        )
        output = proc.stdout + proc.stderr
        if proc.returncode != 0:
            return {"status": "FAIL", "error": f"Lake build returned {proc.returncode}:\n{output}"}

        checked_theorems = parse_axiom_audit_output(output)

        missing_theorems = [t for t in EXPECTED_THEOREMS if t not in checked_theorems]
        if missing_theorems:
            return {
                "status": "FAIL",
                "error": f"Kernel axiom check did not verify expected theorems: {missing_theorems}",
            }

        return {
            "status": "PASS",
            "lake_binary": lake_bin,
            "kernel_checked_theorems": len(checked_theorems),
            "theorems_audited": list(checked_theorems.keys()),
            "axioms_audit": "CLEAN",
        }
    except Exception as e:
        return {"status": "FAIL", "error": f"Exception executing Lake kernel audit: {e}"}

def run_audit(base_dir: Path = None) -> dict:
    if base_dir is None:
        cur = Path(__file__).resolve().parent
        if cur.name == "scripts":
            base_dir = cur.parent
        else:
            base_dir = cur

    src_res = audit_source_files(base_dir)
    lake_res = run_lake_audit(base_dir)

    all_passed = (src_res.get("status") == "PASS") and (lake_res.get("status") == "PASS")

    return {
        "source_audit": src_res,
        "lake_audit": lake_res,
        "theorems_verified": src_res.get("theorem_count", 0),
        "all_passed": all_passed,
    }

if __name__ == "__main__":
    res = run_audit()
    print("=" * 60)
    print("AXIOM AUDIT REPORT")
    print(f"  Scanned Lean files: {res['source_audit'].get('scanned_files_count')}")
    print(f"  Theorems verified:  {res['theorems_verified']} (expected {len(EXPECTED_THEOREMS)})")
    print(f"  Source hygiene:     {res['source_audit'].get('status')} ({res['source_audit'].get('forbidden_audit')})")
    print(f"  Lake kernel build:  {res['lake_audit'].get('status')}")
    if res['lake_audit'].get('status') == 'PASS':
        print(f"  Kernel check count: {res['lake_audit'].get('kernel_checked_theorems')} theorems")
        print(f"  Axioms allowlist:   {res['lake_audit'].get('axioms_audit')}")
    else:
        print(f"  Kernel failure:     {res['lake_audit'].get('error')}")

    if not res["all_passed"]:
        print("\nGATE FAILED: Audit did not pass all strict kernel & source requirements.")
        sys.exit(1)

    print("\nSUCCESS: 0 sorry, 0 admit, 0 custom axioms across all verified theorems.")
    print("=" * 60)
    sys.exit(0)
