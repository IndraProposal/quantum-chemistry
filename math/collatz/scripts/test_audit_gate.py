#!/usr/bin/env python3
"""
Unit Test Gate for Axiom Audit & Theorem Integrity (MIN-85 / PRD-27)

Runs under standard Python `unittest`.
Ensures:
- All 54 theorems are present in Syracuse formalization.
- Zero forbidden tokens (`sorry`, `admit`, `unsafe`, custom axioms) across all Lean files.
- Lake kernel build and `#print axioms` pass with zero custom axioms and allowlisted foundations.
"""

import unittest
from pathlib import Path

# Support running directly or from repository root
try:
    from check_audit import run_audit, EXPECTED_THEOREMS
except ImportError:
    from math.collatz.scripts.check_audit import run_audit, EXPECTED_THEOREMS

class TestAxiomAuditGate(unittest.TestCase):
    def setUp(self):
        script_dir = Path(__file__).resolve().parent
        self.collatz_dir = script_dir.parent

    def test_audit_gate(self):
        res = run_audit(self.collatz_dir)
        self.assertTrue(
            res["all_passed"],
            f"Axiom audit check did not pass all gates: lake={res['lake_audit']}, source={res['source_audit']}"
        )
        self.assertEqual(
            res["theorems_verified"],
            len(EXPECTED_THEOREMS),
            f"Expected {len(EXPECTED_THEOREMS)} theorems, but found {res['theorems_verified']}"
        )
        self.assertEqual(res["source_audit"]["forbidden_audit"], "CLEAN")
        self.assertEqual(res["lake_audit"]["status"], "PASS")
        self.assertEqual(res["lake_audit"]["axioms_audit"], "CLEAN")
        self.assertGreaterEqual(res["lake_audit"]["kernel_checked_theorems"], len(EXPECTED_THEOREMS))

if __name__ == "__main__":
    unittest.main()
