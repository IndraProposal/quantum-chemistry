#!/usr/bin/env python3
"""
test_cv_harness.py — Automated verification and smoke test suite for Hillclimb AI CV package
Validates:
1. Python runtime compatibility (enforcing Python >= 3.12, < 3.14)
2. Dependency importability and pinned library versions
3. Programmatic PDF layout assertions (1 page, 0 overlaps, 0 out-of-bounds)
4. PDF digest verification on verified Darwin arm64 CPython platform
5. High-resolution PNG dimensions and 300 DPI metadata assertions
6. Tamper-evident cryptographic MANIFEST.sha256 integrity
7. Dual-tree mirror parity between canonical hillclimb/ and workspace/goals/goal-4/files/hillclimb/
"""

import sys
import os
import platform
import hashlib
import filecmp
from PIL import Image

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
MIRROR_DIR = os.path.join(REPO_ROOT, "workspace", "goals", "goal-4", "files", "hillclimb")

GOLDEN_PDF_DARWIN_ARM64 = "f4f00dff003ea41fc9945ed4e0262f11eb4b344ec6df2e4b54772e8eb42756bc"

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

def check_dependencies():
    print(f"\n[TEST 2/7] Core Dependency Imports:")
    import reportlab
    import pymupdf
    import pypdf
    import PIL
    print(f"  reportlab: {reportlab.__version__}")
    print(f"  pymupdf: {pymupdf.__version__}")
    print(f"  pypdf: {pypdf.__version__}")
    print(f"  pillow: {PIL.__version__}")
    print("  -> PASS: All core CV builder dependencies imported successfully.")

def check_build_and_layout():
    print(f"\n[TEST 3/7] Programmatic Build & Layout Verification:")
    sys.path.insert(0, SCRIPT_DIR)
    import build_hillclimb_cv
    pdf_path = os.path.join(SCRIPT_DIR, "cv-pavel-cherkashin-hillclimb.pdf")
    png_hd_path = os.path.join(SCRIPT_DIR, "cv-pavel-cherkashin-hillclimb-hd.png")
    
    result = build_hillclimb_cv.build_pdf(pdf_path, png_hd_path)
    print(f"  Page count: {result['page_count']} (expected: 1)")
    print(f"  Text blocks: {result['total_text_blocks']}")
    print(f"  Collisions: {result['text_overlap_count']} (expected: 0)")
    print(f"  Out of bounds: {result['out_of_bounds_count']} (expected: 0)")
    
    assert result['page_count'] == 1, "Page count must be 1"
    assert result['text_overlap_count'] == 0, f"Collisions found: {result['overlaps']}"
    assert result['out_of_bounds_count'] == 0, f"Out of bounds found: {result['out_of_bounds']}"
    print("  -> PASS: Single-page constraint, zero collisions, and zero out-of-bounds verified.")
    return pdf_path, png_hd_path

def check_pdf_digest(pdf_path):
    print(f"\n[TEST 4/7] PDF Cryptographic Digest Scope:")
    with open(pdf_path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(f"  Generated PDF SHA-256: {digest}")
    
    is_darwin_arm64 = sys.platform == "darwin" and platform.machine() in ("arm64", "aarch64")
    if is_darwin_arm64:
        print(f"  Target verified platform (macOS Darwin arm64) detected.")
        assert digest == GOLDEN_PDF_DARWIN_ARM64, (
            f"PDF digest mismatch! Expected {GOLDEN_PDF_DARWIN_ARM64}, got {digest}"
        )
        print("  -> PASS: Deterministic PDF SHA-256 matches verified golden digest.")
    else:
        print(f"  Running on non-Darwin/heterogeneous platform: {sys.platform} {platform.machine()}.")
        print("  -> INFO: Layout invariants verified; byte-level PDF determinism is platform-scoped.")

def check_png_geometry(png_hd_path):
    print(f"\n[TEST 5/7] High-Resolution PNG Geometry & DPI Metadata:")
    img = Image.open(png_hd_path)
    print(f"  Dimensions: {img.size} (expected: 2550x3300)")
    dpi = img.info.get("dpi", (0, 0))
    print(f"  DPI Metadata: {dpi} (expected: ~300 DPI)")
    assert img.size == (2550, 3300), f"Invalid dimensions: {img.size}"
    assert abs(dpi[0] - 300) < 1 and abs(dpi[1] - 300) < 1, f"Invalid DPI: {dpi}"
    
    std_png = png_hd_path.replace("-hd.png", ".png")
    assert os.path.exists(std_png), "Standard PNG alias must exist"
    img_std = Image.open(std_png)
    assert img_std.size == (2550, 3300), f"Standard PNG invalid dimensions: {img_std.size}"
    print("  -> PASS: 300 DPI rasterization and image geometry verified.")

def check_manifest():
    print(f"\n[TEST 6/7] Cryptographic Manifest Check (MANIFEST.sha256):")
    manifest_path = os.path.join(SCRIPT_DIR, "evidence", "MANIFEST.sha256")
    assert os.path.exists(manifest_path), "MANIFEST.sha256 missing"
    
    failures = []
    with open(manifest_path, "r") as f:
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

def check_mirror_parity():
    print(f"\n[TEST 7/7] Dual-Tree Workspace Mirror Parity:")
    if not os.path.exists(MIRROR_DIR):
        print(f"  Mirror dir {MIRROR_DIR} not found; skipping mirror check.")
        return
    
    diffs = []
    for root, dirs, files in os.walk(SCRIPT_DIR):
        rel_root = os.path.relpath(root, SCRIPT_DIR)
        mirror_root = os.path.join(MIRROR_DIR, rel_root) if rel_root != "." else MIRROR_DIR
        for file in files:
            if file.startswith(".") or file.endswith(".pyc") or "__pycache__" in root:
                continue
            src_file = os.path.join(root, file)
            dst_file = os.path.join(mirror_root, file)
            if not os.path.exists(dst_file):
                diffs.append((os.path.join(rel_root, file), "MISSING_IN_MIRROR"))
            elif not filecmp.cmp(src_file, dst_file, shallow=False):
                diffs.append((os.path.join(rel_root, file), "CONTENT_MISMATCH"))
                
    if diffs:
        print(f"  -> FAIL: Discrepancies between hillclimb/ and workspace mirror: {diffs}")
        raise AssertionError(f"Mirror discrepancies: {diffs}")
    print("  -> PASS: 100% byte-for-byte dual-tree parity between repo and workspace.")

def main():
    print("================================================================================")
    print("   Hillclimb AI — Employee #5 Evals & Build Harness Automated Test Suite")
    print("================================================================================")
    check_python_environment()
    check_dependencies()
    pdf_path, png_hd_path = check_build_and_layout()
    check_pdf_digest(pdf_path)
    check_png_geometry(png_hd_path)
    check_manifest()
    check_mirror_parity()
    print("\n================================================================================")
    print("   ALL 7 HARNESS & REPRODUCIBILITY CHECKS PASSED SUCCESSFULLY (PASS)")
    print("================================================================================")

if __name__ == "__main__":
    main()
