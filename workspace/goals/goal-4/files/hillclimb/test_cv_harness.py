#!/usr/bin/env python3
"""
test_cv_harness.py — Automated verification and smoke test suite for Hillclimb AI CV package
Validates:
1. Python runtime compatibility (enforcing Python >= 3.12, < 3.14)
2. Dependency importability and pinned library versions (strictly verified against requirements.lock)
3. Programmatic PDF layout assertions in an isolated temporary sandbox (1 page, 0 overlaps, 0 out-of-bounds)
4. PDF digest verification across verified platforms (macOS Darwin arm64 and Linux x86_64)
5. High-resolution PNG dimensions and 300 DPI metadata assertions
6. Tamper-evident cryptographic MANIFEST.sha256 integrity
7. Bidirectional dual-tree mirror parity between canonical hillclimb/ and workspace/goals/goal-4/files/hillclimb/
"""

import sys
import os

# Prevent bytecode generation (.pyc / __pycache__) to avoid workspace pollution
sys.dont_write_bytecode = True

import platform
import hashlib
import filecmp
import tempfile
import shutil
import subprocess
import importlib.metadata
import unittest
from unittest.mock import patch
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
MIRROR_DIR = os.path.join(REPO_ROOT, "workspace", "goals", "goal-4", "files", "hillclimb")

# Architecture alias mapping to canonical representations
ARCH_CANONICAL_ALIASES = {
    "arm64": "aarch64",
    "aarch64": "aarch64",
    "x86_64": "x86_64",
    "amd64": "x86_64",
}

def normalize_platform_key(plat=None, mach=None):
    """
    Normalizes OS and architecture into a canonical platform key (e.g. linux_x86_64, darwin_aarch64).
    Maps known architecture aliases (arm64 -> aarch64, amd64 -> x86_64).
    """
    if plat is None:
        plat = sys.platform
    if mach is None:
        mach = platform.machine()
        
    os_name = "linux" if plat.startswith("linux") else plat.lower()
    mach_lower = mach.lower()
    canonical_mach = ARCH_CANONICAL_ALIASES.get(mach_lower, mach_lower)
    return f"{os_name}_{canonical_mach}"

# Verified golden PDF SHA-256 digests across verified deterministic CPython environments
# Strictly registered keys for verified target architectures (Darwin Apple Silicon and Linux x86_64 / aarch64)
VERIFIED_GOLDEN_PDF_DIGESTS = {
    "darwin_aarch64": "f4f00dff003ea41fc9945ed4e0262f11eb4b344ec6df2e4b54772e8eb42756bc",
    "darwin_arm64": "f4f00dff003ea41fc9945ed4e0262f11eb4b344ec6df2e4b54772e8eb42756bc",
    "linux_x86_64": "f4f00dff003ea41fc9945ed4e0262f11eb4b344ec6df2e4b54772e8eb42756bc",
    "linux_amd64": "f4f00dff003ea41fc9945ed4e0262f11eb4b344ec6df2e4b54772e8eb42756bc",
    "linux_aarch64": "f4f00dff003ea41fc9945ed4e0262f11eb4b344ec6df2e4b54772e8eb42756bc",
    "linux_arm64": "f4f00dff003ea41fc9945ed4e0262f11eb4b344ec6df2e4b54772e8eb42756bc",
}

# Core CV builder libraries and expected pinned versions
CORE_PINNED_VERSIONS = {
    "reportlab": "5.1.0",
    "pymupdf": "2.0",
    "pypdf": "6.21.2",
    "pillow": "12.3.0",
}

def get_git_status():
    """Captures working tree status via git status --porcelain, if in a git repository."""
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False
        )
        if res.returncode == 0:
            return res.stdout
    except Exception:
        pass
    return None

def check_python_environment():
    print(f"[TEST 1/7] Python Runtime Environment:")
    print(f"  Version: {sys.version.split()[0]} ({sys.version})")
    print(f"  Platform: {platform.platform()} ({platform.machine()})")
    print(f"  Executable: {sys.executable}")
    if sys.version_info < (3, 12) or sys.version_info >= (3, 14):
        raise RuntimeError(
            f"Unsupported Python version {sys.version.split()[0]}. "
            f"Verified lockfile dependencies require Python >= 3.12, < 3.14."
        )
    print("  -> PASS: Python version satisfies >= 3.12, < 3.14 constraint.")
    return "PASS"

def check_dependencies():
    print(f"\n[TEST 2/7] Core Dependency Imports & Pinned Version Verification:")
    import reportlab
    import pymupdf
    import pypdf
    import PIL
    
    # 1. Direct core package version checks
    for mod_name, expected_ver in CORE_PINNED_VERSIONS.items():
        if mod_name == "pillow":
            actual_ver = getattr(PIL, "__version__", None)
        else:
            mod = sys.modules.get(mod_name)
            actual_ver = getattr(mod, "__version__", None)
            
        print(f"  {mod_name}: installed {actual_ver} (pinned: {expected_ver})")
        assert actual_ver == expected_ver, (
            f"Core dependency version mismatch for '{mod_name}': "
            f"expected {expected_ver}, got {actual_ver}"
        )
        
    # 2. Transitive lockfile check against requirements.lock
    lockfile_path = os.path.join(SCRIPT_DIR, "requirements.lock")
    if os.path.exists(lockfile_path):
        print(f"  Checking installed packages against requirements.lock:")
        lock_mismatches = []
        with open(lockfile_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "==" not in line:
                    continue
                pkg_name, pinned_ver = [part.strip() for part in line.split("==", 1)]
                try:
                    installed_ver = importlib.metadata.version(pkg_name)
                    if installed_ver != pinned_ver:
                        lock_mismatches.append(f"{pkg_name}: expected {pinned_ver}, installed {installed_ver}")
                    else:
                        print(f"    [LOCK OK] {pkg_name} == {installed_ver}")
                except importlib.metadata.PackageNotFoundError:
                    lock_mismatches.append(f"{pkg_name}: NOT_INSTALLED (expected {pinned_ver})")
                    
        if lock_mismatches:
            raise AssertionError(
                f"Lockfile pinned version discrepancies detected ({len(lock_mismatches)}):\n"
                + "\n".join(f"    - {m}" for m in lock_mismatches)
            )
        print("  -> PASS: All locked library versions in requirements.lock verified strictly.")
    else:
        print("  -> PASS: All core CV builder pinned library versions verified.")
    return "PASS"

def check_build_and_layout(temp_dir):
    print(f"\n[TEST 3/7] Programmatic Build & Layout Verification (Isolated Temp Sandbox):")
    sys.path.insert(0, SCRIPT_DIR)
    import build_hillclimb_cv
    
    temp_pdf = os.path.join(temp_dir, "cv-pavel-cherkashin-hillclimb.pdf")
    temp_png_hd = os.path.join(temp_dir, "cv-pavel-cherkashin-hillclimb-hd.png")
    
    result = build_hillclimb_cv.build_pdf(temp_pdf, temp_png_hd, sync_to_mirror=False)
    print(f"  Page count: {result['page_count']} (expected: 1)")
    print(f"  Text blocks: {result['total_text_blocks']}")
    print(f"  Collisions: {result['text_overlap_count']} (expected: 0)")
    print(f"  Out of bounds: {result['out_of_bounds_count']} (expected: 0)")
    
    assert result['page_count'] == 1, "Page count must be 1"
    assert result['text_overlap_count'] == 0, f"Collisions found: {result['overlaps']}"
    assert result['out_of_bounds_count'] == 0, f"Out of bounds found: {result['out_of_bounds']}"
    print("  -> PASS: Single-page constraint, zero collisions, and zero out-of-bounds verified.")
    return temp_pdf, temp_png_hd

def check_pdf_digest(pdf_path, platform_override=None, machine_override=None):
    print(f"\n[TEST 4/7] PDF Cryptographic Digest Scope:")
    with open(pdf_path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(f"  Generated PDF SHA-256: {digest}")
    
    plat = platform_override if platform_override is not None else sys.platform
    mach = machine_override if machine_override is not None else platform.machine()
    
    # 1. Direct raw lookup (e.g. darwin_arm64, linux_x86_64)
    raw_key = f"{plat}_{mach.lower()}"
    # 2. Canonical normalized architecture lookup (e.g. arm64 -> aarch64, amd64 -> x86_64)
    norm_key = normalize_platform_key(plat, mach)
    
    expected_golden = VERIFIED_GOLDEN_PDF_DIGESTS.get(norm_key) or VERIFIED_GOLDEN_PDF_DIGESTS.get(raw_key)
    
    # Explicit constraint: NO blanket fallback to linux_x86_64 or any generic profile.
    # Unregistered Linux or POSIX architectures (riscv64, ppc64le, s390x, etc.) strictly yield SKIP.
    if expected_golden:
        print(f"  Verified target platform: {plat} ({mach}) -> canonical key: {norm_key}")
        print(f"  Expected Golden SHA-256: {expected_golden}")
        assert digest == expected_golden, (
            f"PDF digest mismatch! Expected {expected_golden}, got {digest}"
        )
        print("  -> PASS: Deterministic PDF SHA-256 matches verified golden digest.")
        return "PASS"
    else:
        print(f"  Running on unverified/heterogeneous platform: {plat} {mach} (canonical key: {norm_key}).")
        print("  -> SKIP: PDF byte-level golden digest assertion is platform-scoped and skipped on this host.")
        return "SKIP"

def check_png_geometry(png_hd_path):
    print(f"\n[TEST 5/7] High-Resolution PNG Geometry & DPI Metadata:")
    with Image.open(png_hd_path) as img:
        print(f"  Dimensions: {img.size} (expected: 2550x3300)")
        dpi = img.info.get("dpi", (0, 0))
        print(f"  DPI Metadata: {dpi} (expected: ~300 DPI)")
        assert img.size == (2550, 3300), f"Invalid dimensions: {img.size}"
        assert abs(dpi[0] - 300) < 1 and abs(dpi[1] - 300) < 1, f"Invalid DPI: {dpi}"
    
    std_png = png_hd_path.replace("-hd.png", ".png")
    assert os.path.exists(std_png), "Standard PNG alias must exist in test output"
    with Image.open(std_png) as img_std:
        assert img_std.size == (2550, 3300), f"Standard PNG invalid dimensions: {img_std.size}"
    print("  -> PASS: 300 DPI rasterization and image geometry verified.")
    return "PASS"

def check_manifest():
    print(f"\n[TEST 6/7] Cryptographic Manifest Check (MANIFEST.sha256):")
    manifest_path = os.path.join(SCRIPT_DIR, "evidence", "MANIFEST.sha256")
    assert os.path.exists(manifest_path), "MANIFEST.sha256 missing"
    
    failures = []
    with open(manifest_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            if len(parts) != 2:
                continue
            expected_hash, rel_file = parts
            target_path = os.path.join(SCRIPT_DIR, rel_file)
            if not os.path.exists(target_path):
                failures.append((rel_file, "FILE_NOT_FOUND"))
                continue
            with open(target_path, "rb") as tf:
                actual_hash = hashlib.sha256(tf.read()).hexdigest()
            if actual_hash != expected_hash:
                failures.append((rel_file, f"HASH_MISMATCH: expected {expected_hash[:10]}..., got {actual_hash[:10]}..."))
            else:
                print(f"  [OK] {rel_file}: {actual_hash[:12]}...")
                
    if failures:
        print(f"  -> FAIL: Manifest verification failures: {failures}")
        raise AssertionError(f"Manifest verification failed for {len(failures)} entries: {failures}")
    print("  -> PASS: All manifest entries verified.")
    return "PASS"

def check_mirror_parity():
    print(f"\n[TEST 7/7] Bidirectional Dual-Tree Workspace Mirror Parity:")
    if not os.path.exists(MIRROR_DIR):
        print(f"  Mirror dir {MIRROR_DIR} not found; skipping mirror check.")
        return "SKIP"
    
    def collect_rel_files(base_dir):
        rel_files = set()
        for root, dirs, files in os.walk(base_dir):
            if "__pycache__" in root:
                continue
            parts = os.path.relpath(root, base_dir).split(os.sep)
            if any(p.startswith(".") for p in parts if p != "."):
                continue
            for file in files:
                if file.startswith(".") or file.endswith(".pyc") or file == ".DS_Store":
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                rel_files.add(rel_path)
        return rel_files

    canonical_files = collect_rel_files(SCRIPT_DIR)
    mirror_files = collect_rel_files(MIRROR_DIR)
    
    diffs = []
    missing_in_mirror = canonical_files - mirror_files
    for f in sorted(missing_in_mirror):
        diffs.append((f, "MISSING_IN_MIRROR"))
        
    extra_in_mirror = mirror_files - canonical_files
    for f in sorted(extra_in_mirror):
        diffs.append((f, "EXTRA_IN_MIRROR"))
        
    common_files = canonical_files & mirror_files
    for f in sorted(common_files):
        src_file = os.path.join(SCRIPT_DIR, f)
        dst_file = os.path.join(MIRROR_DIR, f)
        if not filecmp.cmp(src_file, dst_file, shallow=False):
            diffs.append((f, "CONTENT_MISMATCH"))
            
    if diffs:
        print(f"  -> FAIL: Bidirectional discrepancies between hillclimb/ and workspace mirror: {diffs}")
        raise AssertionError(f"Bidirectional mirror discrepancies found ({len(diffs)}): {diffs}")
        
    print(f"  Total canonical files: {len(canonical_files)}")
    print(f"  Total mirror files: {len(mirror_files)}")
    print(f"  -> PASS: 100% byte-for-byte bidirectional dual-tree parity verified ({len(common_files)} files).")
    return "PASS"

def cleanup_bytecode():
    """Removes any inadvertently generated __pycache__ folders in SCRIPT_DIR."""
    for root, dirs, files in os.walk(SCRIPT_DIR, topdown=False):
        for d in dirs:
            if d == "__pycache__":
                try:
                    shutil.rmtree(os.path.join(root, d))
                except Exception:
                    pass

def run_harness(platform_override=None, machine_override=None, suite_label="Hillclimb AI — Employee #5 Evals & Build Harness Automated Test Suite"):
    print("================================================================================")
    print(f"   {suite_label}")
    if platform_override or machine_override:
        sim_plat = platform_override or sys.platform
        sim_mach = machine_override or platform.machine()
        print(f"   [Simulation Mode: sys.platform='{sim_plat}', platform.machine()='{sim_mach}']")
    print("================================================================================")
    
    # Capture initial git status for regression assertion
    git_status_before = get_git_status()
    
    temp_dir = tempfile.mkdtemp(prefix="hillclimb_cv_test_")
    test_results = {}
    
    try:
        test_results["1_python_env"] = check_python_environment()
        test_results["2_dependencies"] = check_dependencies()
        temp_pdf, temp_png_hd = check_build_and_layout(temp_dir)
        test_results["3_build_layout"] = "PASS"
        test_results["4_pdf_digest"] = check_pdf_digest(
            temp_pdf,
            platform_override=platform_override,
            machine_override=machine_override
        )
        test_results["5_png_geometry"] = check_png_geometry(temp_png_hd)
        test_results["6_manifest"] = check_manifest()
        test_results["7_mirror_parity"] = check_mirror_parity()
        
        passed_count = sum(1 for s in test_results.values() if s == "PASS")
        skipped_count = sum(1 for s in test_results.values() if s == "SKIP")
        total_count = len(test_results)
        
        print("\n================================================================================")
        if skipped_count == 0:
            print(f"   ALL {total_count} HARNESS & REPRODUCIBILITY CHECKS PASSED SUCCESSFULLY ({passed_count} passed, 0 skipped)")
        else:
            print(f"   HARNESS COMPLETED: {passed_count} PASSED, {skipped_count} SKIPPED (ALL ACTIVE ASSERTIONS PASSED)")
        print("================================================================================")
        return passed_count, skipped_count, test_results
        
    finally:
        # Guarantee removal of temporary sandbox files
        shutil.rmtree(temp_dir, ignore_errors=True)
        cleanup_bytecode()
        
        # Regression assertion: verify working tree git status remains 100% unchanged
        git_status_after = get_git_status()
        if git_status_before is not None and git_status_after is not None:
            assert git_status_before == git_status_after, (
                f"Regression Error: Working tree git status modified during test execution!\n"
                f"Before:\n{git_status_before}\n"
                f"After:\n{git_status_after}"
            )
            print("   REGRESSION ASSERTION: git status --porcelain is identical before and after test run (PASS)")
            print("================================================================================")

def test_mocked_unregistered_linux_platform():
    """
    Automated test with mocked unknown Linux platform.machine() (e.g. riscv64).
    Confirms that check_pdf_digest() returns SKIP on unrecognized architectures
    and that the overall test suite counter reports exactly 6 passed, 1 skipped.
    """
    print("\n================================================================================")
    print("   AUTOMATED TEST: Unregistered Linux Architecture SKIP Verification")
    print("   (Simulating platform.machine() == 'riscv64' under sys.platform == 'linux')")
    print("================================================================================")
    
    passed_count, skipped_count, results = run_harness(
        platform_override="linux",
        machine_override="riscv64",
        suite_label="Mocked Linux Architecture Test (riscv64)"
    )
    
    assert results["4_pdf_digest"] == "SKIP", (
        f"Assertion Failed: check_pdf_digest returned '{results['4_pdf_digest']}', expected 'SKIP'!"
    )
    assert passed_count == 6, (
        f"Assertion Failed: expected 6 passed tests, got {passed_count} ({results})"
    )
    assert skipped_count == 1, (
        f"Assertion Failed: expected 1 skipped test, got {skipped_count} ({results})"
    )
    print("\n   [MOCK TEST VERIFICATION SUCCESSFUL]")
    print("   -> Confirmed: Unregistered Linux machine ('riscv64') returns SKIP for PDF digest.")
    print(f"   -> Confirmed: Test counter strictly reports {passed_count} passed, {skipped_count} skipped.")
    print("================================================================================\n")

class TestCvHarnessReproducibility(unittest.TestCase):
    """Unit test suite verifying cross-platform digest routing and SKIP behaviors."""
    
    def test_unregistered_linux_machines_return_skip(self):
        """Verifies that unknown Linux architectures (riscv64, ppc64le, s390x, mips64) return SKIP and 6 passed, 1 skipped."""
        for unknown_arch in ["riscv64", "ppc64le", "s390x", "mips64"]:
            with self.subTest(arch=unknown_arch):
                passed_cnt, skipped_cnt, results = run_harness(
                    platform_override="linux",
                    machine_override=unknown_arch,
                    suite_label=f"Mocked Linux '{unknown_arch}' Architecture Verification"
                )
                self.assertEqual(results["4_pdf_digest"], "SKIP")
                self.assertEqual(passed_cnt, 6)
                self.assertEqual(skipped_cnt, 1)

    def test_linux_arm64_alias_normalization(self):
        """Verifies that Linux reporting 'arm64' normalizes to 'aarch64' and matches golden digest."""
        key = normalize_platform_key("linux", "arm64")
        self.assertEqual(key, "linux_aarch64")
        self.assertIn(key, VERIFIED_GOLDEN_PDF_DIGESTS)
        
    def test_unknown_darwin_machine_returns_skip(self):
        """Verifies that unknown Darwin architectures return SKIP."""
        key = normalize_platform_key("darwin", "ppc")
        self.assertNotIn(key, VERIFIED_GOLDEN_PDF_DIGESTS)

def main():
    if "--unittest" in sys.argv:
        # Run unittest test runner
        sys.argv.remove("--unittest")
        unittest.main()
        return
        
    if "--mock-only" in sys.argv or "--test-mock-skip" in sys.argv:
        # Run isolated mock SKIP test
        test_mocked_unregistered_linux_platform()
        return
        
    # 1. Primary execution on native host platform
    run_harness()
    
    # 2. Automated test verifying unregistered Linux platform behavior (6 passed, 1 skipped)
    test_mocked_unregistered_linux_platform()

if __name__ == "__main__":
    main()
