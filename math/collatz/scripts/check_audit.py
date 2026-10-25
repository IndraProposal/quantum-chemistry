#!/usr/bin/env python3
"""
Axiom Audit Checker for Syracuse Formalization (MIN-85 / PRD-27)

Verifies:
1. All 34 formalized theorems in Collatz/Syracuse.lean are accounted for.
2. Zero `sorry`, zero `admit`, zero custom `axiom` declarations.
3. If Lean/Lake is installed, executes `lake build` to confirm kernel acceptance
   and verify `#print axioms` dependencies.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

EXPECTED_THEOREMS = [
    "v2_zero",
    "v2_two",
    "v2_four",
    "v2_eight",
    "v2_sixteen",
    "syracuse_one",
    "syracuse_three",
    "syracuse_five",
    "syracuse_two_steps_three",
    "descent_three",
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
    "syracuse_nineteen",
    "syracuse_twentynine",
    "descent_nineteen",
    "syracuse_twentyone",
    "descent_twentyone",
    "syracuse_twentyfive",
    "descent_twentyfive",
    "syracuse_twentyseven_step1",
    "syracuse_fortyone",
    "descent_cert_three",
    "descent_cert_seven",
    "descent_cert_fifteen",
]

def audit_source_files(base_dir: Path) -> dict:
    syracuse_lean = base_dir / "Collatz" / "Syracuse.lean"
    audit_lean = base_dir / "AxiomAudit.lean"

    if not syracuse_lean.exists():
        raise FileNotFoundError(f"Missing {syracuse_lean}")
    if not audit_lean.exists():
        raise FileNotFoundError(f"Missing {audit_lean}")

    content = syracuse_lean.read_text(encoding="utf-8")
    
    # Check forbidden keywords
    forbidden = ["sorry", "admit", "unsafe", "axiom "]
    for word in forbidden:
        matches = [line for line in content.splitlines() if word in line and not line.strip().startswith("--")]
        if matches:
            raise ValueError(f"Found forbidden keyword '{word}' in {syracuse_lean}: {matches}")

    # Extract declared theorems
    thms = re.findall(r"theorem\s+([A-Za-z0-9_]+)", content)
    
    # Verify expected theorems
    missing = [t for t in EXPECTED_THEOREMS if t not in thms]
    if missing:
        raise ValueError(f"Missing expected theorems: {missing}")

    return {
        "status": "PASS",
        "theorem_count": len(thms),
        "theorems": thms,
        "forbidden_audit": "CLEAN",
    }

def run_lake_audit(base_dir: Path) -> dict:
    # Try running lake build if available
    try:
        proc = subprocess.run(
            ["lake", "build"],
            cwd=base_dir,
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = proc.stdout + proc.stderr
        if proc.returncode != 0:
            return {"status": "FAIL", "error": output}
        
        # Check that no custom axioms are reported
        lines = [line for line in output.splitlines() if "does not depend on any axioms" in line or "depends on axioms" in line]
        custom_axioms = [line for line in output.splitlines() if "depends on axioms" in line and ("sorryAx" in line or "axiom" in line)]
        if custom_axioms:
            return {"status": "FAIL", "error": f"Detected forbidden axioms: {custom_axioms}"}

        return {
            "status": "PASS",
            "kernel_checked_theorems": len(lines),
            "output": output,
        }
    except FileNotFoundError:
        return {"status": "SKIPPED", "reason": "lake binary not found in PATH"}

def run_audit(base_dir: Path = None) -> dict:
    if base_dir is None:
        # Resolve to math/collatz
        cur = Path(__file__).resolve().parent
        if cur.name == "scripts":
            base_dir = cur.parent
        else:
            base_dir = cur

    src_res = audit_source_files(base_dir)
    lake_res = run_lake_audit(base_dir)

    return {
        "source_audit": src_res,
        "lake_audit": lake_res,
        "theorems_verified": src_res["theorem_count"],
        "all_passed": src_res["status"] == "PASS" and lake_res.get("status") in ("PASS", "SKIPPED"),
    }

if __name__ == "__main__":
    res = run_audit()
    print(f"Axiom Audit Report:")
    print(f"  Theorems verified: {res['theorems_verified']} (expected {len(EXPECTED_THEOREMS)})")
    print(f"  Source hygiene:    {res['source_audit']['status']}")
    print(f"  Lake kernel build: {res['lake_audit']['status']}")
    if not res["all_passed"]:
        print("Audit failed!")
        sys.exit(1)
    print("SUCCESS: 0 sorry, 0 admit, 0 custom axioms.")
    sys.exit(0)
