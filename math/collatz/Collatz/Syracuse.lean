/-
Copyright (c) 2026 Mindrock. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: agy (Wolfram)
-/

namespace Collatz

/-- Helper fuel-based 2-adic valuation for structural kernel reduction. -/
def v2Aux : Nat → Nat → Nat
  | 0, _ => 0
  | fuel + 1, n =>
    if n % 2 = 0 ∧ n > 0 then
      1 + v2Aux fuel (n / 2)
    else
      0

/-- 2-adic valuation v2(n) of natural number n. -/
def v2 (n : Nat) : Nat := v2Aux n n

/-- Accelerated Syracuse map S(n) = (3n + 1) / 2^(v2(3n + 1)). -/
def S (n : Nat) : Nat :=
  let m := 3 * n + 1
  m / 2^(v2 m)

/-- k-step Syracuse iteration S^[k](n). -/
def iterateS : Nat → Nat → Nat
  | 0, n => n
  | k + 1, n => S (iterateS k n)

/-- Machine-verifiable certificate checker: tests if S^[k](n) < n for k > 0. -/
def verifyCertificate (n : Nat) (k : Nat) : Bool :=
  if k == 0 then false
  else
    let v := iterateS k n
    v < n

/-- Proposition: n reaches descent below n in finite steps k > 0. -/
def HasDescent (n : Nat) : Prop :=
  ∃ k : Nat, k > 0 ∧ iterateS k n < n

/-!
### Section 1: Foundational Valuations and Invariants
-/

-- Theorem 1: v2 of zero
theorem v2_zero : v2 0 = 0 := by rfl

-- Theorem 2: v2 of 2
theorem v2_two : v2 2 = 1 := by rfl

-- Theorem 3: v2 of 4
theorem v2_four : v2 4 = 2 := by rfl

-- Theorem 4: v2 of 8
theorem v2_eight : v2 8 = 3 := by rfl

-- Theorem 5: v2 of 16
theorem v2_sixteen : v2 16 = 4 := by rfl

/-!
### Section 2: Fixed Point and Elementary Orbits
-/

-- Theorem 6: Fixed point of Syracuse map at 1
theorem syracuse_one : S 1 = 1 := by rfl

-- Theorem 7: Orbit step from 3 to 5
theorem syracuse_three : S 3 = 5 := by rfl

-- Theorem 8: Orbit step from 5 to 1
theorem syracuse_five : S 5 = 1 := by rfl

-- Theorem 9: Two-step orbit from 3 reaches 1
theorem syracuse_two_steps_three : iterateS 2 3 = 1 := by rfl

-- Theorem 10: Strict descent for n = 3 in 2 steps
theorem descent_three : iterateS 2 3 < 3 := by decide

/-!
### Section 3: Deep Orbits (7 and 15)
-/

-- Theorem 11: Orbit step from 7 to 11
theorem syracuse_seven : S 7 = 11 := by rfl

-- Theorem 12: Orbit step from 11 to 17
theorem syracuse_eleven : S 11 = 17 := by rfl

-- Theorem 13: Orbit step from 17 to 13
theorem syracuse_seventeen : S 17 = 13 := by rfl

-- Theorem 14: Orbit step from 13 to 5
theorem syracuse_thirteen : S 13 = 5 := by rfl

-- Theorem 15: Descent for n = 7 at step 4 (5 < 7)
theorem descent_seven : iterateS 4 7 < 7 := by decide

-- Theorem 16: Orbit step from 9 to 7
theorem syracuse_nine : S 9 = 7 := by rfl

-- Theorem 17: Descent for n = 9 in 1 step (7 < 9)
theorem descent_nine : iterateS 1 9 < 9 := by decide

-- Theorem 18: Orbit step from 15 to 23
theorem syracuse_fifteen : S 15 = 23 := by rfl

-- Theorem 19: Orbit step from 23 to 35
theorem syracuse_twentythree : S 23 = 35 := by rfl

-- Theorem 20: Orbit step from 35 to 53
theorem syracuse_thirtyfive : S 35 = 53 := by rfl

-- Theorem 21: Orbit step from 53 to 5
theorem syracuse_fiftythree : S 53 = 5 := by rfl

-- Theorem 22: Descent for n = 15 at step 5 (5 < 15)
theorem descent_fifteen : iterateS 5 15 < 15 := by decide

/-!
### Section 4: Odd Orbits (19, 21, 25, 27)
-/

-- Theorem 23: Orbit step from 19 to 29
theorem syracuse_nineteen : S 19 = 29 := by rfl

-- Theorem 24: Orbit step from 29 to 11
theorem syracuse_twentynine : S 29 = 11 := by rfl

-- Theorem 25: Descent for n = 19 in 3 steps (11 < 19)
theorem descent_nineteen : iterateS 3 19 < 19 := by decide

-- Theorem 26: Immediate descent step for n = 21 (S(21) = 1)
theorem syracuse_twentyone : S 21 = 1 := by rfl

-- Theorem 27: Descent for n = 21 in 1 step (1 < 21)
theorem descent_twentyone : iterateS 1 21 < 21 := by decide

-- Theorem 28: Immediate descent step for n = 25 (S(25) = 19)
theorem syracuse_twentyfive : S 25 = 19 := by rfl

-- Theorem 29: Descent for n = 25 in 1 step (19 < 25)
theorem descent_twentyfive : iterateS 1 25 < 25 := by decide

-- Theorem 30: 27 orbit step 1 (27 -> 41)
theorem syracuse_twentyseven_step1 : S 27 = 41 := by rfl

-- Theorem 31: Orbit step from 41 to 31
theorem syracuse_fortyone : S 41 = 31 := by rfl

/-!
### Section 5: LEMMA_TARGET Certificates
-/

-- Theorem 32: Valid descent certificate for n = 3 with k = 2
theorem descent_cert_three : verifyCertificate 3 2 = true := by decide

-- Theorem 33: Valid descent certificate for n = 7 with k = 4
theorem descent_cert_seven : verifyCertificate 7 4 = true := by decide

-- Theorem 34: Valid descent certificate for n = 15 with k = 5
theorem descent_cert_fifteen : verifyCertificate 15 5 = true := by decide

end Collatz
