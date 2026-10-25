/-
Copyright (c) 2026 Mindrock. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: agy (Wolfram)
-/
import Collatz.Syracuse

/-!
# Collatz & Syracuse Accelerated Formalization Stack (AMDE-RP-002 / MIN-85)

This module provides the accelerated Syracuse dynamical map:
$$S(n) = \frac{3n + 1}{2^{v_2(3n + 1)}}$$
and machine-verifiable `LEMMA_TARGET` certificates confirming orbit descent below $n$
for odd integers $n > 1$.
-/
