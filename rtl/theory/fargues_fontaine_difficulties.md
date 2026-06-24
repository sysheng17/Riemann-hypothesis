# Fargues-Fontaine Approach to RH: Enumeration of All Difficulties

## Context

Scholze (2023, MPIM talk "What does Spec Z look like?") announced that the
Fargues-Fontaine curve provides a geometric framework for the Riemann Hypothesis.
The idea: the FF curve over Q_p (or its archimedean analogue over C) admits
a canonical metric whose associated Laplacian's spectrum encodes ζ(s) zeros,
and the metric's positivity forces all zeros onto Re(s)=1/2.

No paper has been written. This document enumerates every difficulty between the
announcement and a proof of RH.

---

## 1. No Global FF Curve Over Spec Z

**Statement**: The Fargues-Fontaine curve X_{FF}(E) is defined for each local
field E (either a p-adic field or C). There is **no single FF curve** whose
base is Spec Z. The FF curve is intrinsically per-prime.

**Why this matters**: To apply the geometric proof of RH (analogue of Deligne's
Weil II for function fields), we need a single geometric object
X_{FF}(Spec Z) whose zeta function is ζ(s). Multiple per-prime curves do not
glue. Scholze's talk proposed that the twistor-P¹ supplies the archimedean
component, but no gluing construction across all primes exists.

**Status**: Open. The WCart_Z construction (CRT fiber product of per-p
Cartier-Witt stacks) in `global_wcart_construction.md` is a proposal, not a
proven geometric object with FF-like properties.

---

## 2. Canonical Metric Not Constructed

**Statement**: The canonical metric on X_{FF}(E) is central to the approach.
Scholze's talk asserted its existence, but no construction has been published.

**Known facts**:
- For each p, the FF curve X_{FF}(Q_p) is a complete algebraic curve over Q_p
- There is a natural "Frobenius" automorphism φ_p acting on X_{FF}(Q_p)
- Scholze claimed there is a canonical metric g_{FF} making φ_p an isometry
- This metric would define an L²-space on which the R-action is unitary

**Why this matters**: Without the metric, the R-action's generator cannot be
proven skew-adjoint, and RH does not follow. The metric is the entire content
of the proof — everything else (the operator, the trace formula) already exists
in Deninger's framework.

**Status**: Open and unpublished. The Anschütz-Bosco-LeBras-RodríguezCamargo-
Scholze (2025, v2 2026) paper on analytic de Rham stacks constructs related
objects but does **not** construct this canonical metric.

---

## 3. Continuous Spectrum / Ruelle Obstruction (G5/G7)

**Statement**: Even if the canonical metric exists and the R-action is unitary,
the non-trivial zeros of ζ(s) are **not eigenvalues of the generator Θ**.
They are Ruelle resonances arising from analytic continuation of the Euler
product.

**This is the core obstacle from `remaining_gaps.md` and `ruelle_impossibility_proof.md`:**

```
det_∞(s-Θ) = Π_p (1-p^{-s})⁻¹  (Euler product, Re(s)>1)
           = ζ(s)               (analytic continuation, s ∈ C)
```

The non-trivial zeros appear in the **analytic continuation** step. They are
poles of the analytically continued resolvent (s-Θ)⁻¹, i.e., Ruelle resonances,
not spectral eigenvalues of Θ. No spectral theorem constrains resonances.

**Why the FF metric does not solve this**: The metric defines an L²-space and
may prove Θ is skew-adjoint on that space. But the **discrete spectrum** of Θ
is still {i·log p} (the prime orbits). The non-trivial zeros (γ ≈ ±14.13, ...)
are not in {i·log p}. The identity ζ(s) = det_∞(s-Θ) holds only formally;
equating "zero of ζ(s)" with "eigenvalue of Θ" is a category error — the
zeros are poles of the analytic continuation of (s-Θ)⁻¹, not zeros of (s-Θ).

**This difficulty is independent of the metric. It is structural.**

**Status**: The Ruelle Impossibility Theorem (`ruelle_impossibility_proof.md`,
Theorem 1) proves that any operator satisfying Deninger's trace formula
Tr(e^{tΘ}) = Σ log p·δ(t−log p) has discrete spectrum {i·log p}, and its
Ruelle zeta function's zeros (the non-trivial ζ zeros) are resonances, not
eigenvalues. The FF framework would need to provide an operator that does
**not** satisfy the Deninger trace formula — i.e., a fundamentally different
operator, not the generator of the R-action on the rational Witt space.

---

## 4. Trace Formula Not Derived from FF Geometry

**Statement**: The identity det_∞(s-Θ) = ζ(s) comes from Deninger's dynamical
system (foliated rational Witt space, Selberg-type trace formula). It has not
been derived from the geometry of the FF curve.

**The FF approach claims**: The R-action on the FF curve (or twistor-P¹) has
the same periodic orbits (primes) with the same lengths (log p), so the same
Ruelle determinant identity holds.

**But**: The Deninger trace formula involves ζ-regularization and a specific
cohomology theory (H^1_red of the foliated space). The FF analogue would
require:
- A cohomology theory on X_{FF}(Spec Z)
- A Lefschetz fixed-point formula for the Frobenius action
- An identification of the resulting determinant with ζ(s)

None of these exist.

**Status**: Open. The identity det_∞(s-Θ)=ζ(s) exists in Deninger's framework
but the FF framework would need to reproduce or replace it.

---

## 5. Unitarity of Frobenius Not Proven

**Statement**: In the function field case (curves C/F_q), Deligne proved that
Frobenius acts on ℓ-adic cohomology with eigenvalues of absolute value q^{w/2}
(purity theorem, Weil II). This is the heart of RH for function fields.

**Analogue for the FF approach**: The Frobenius φ_p on X_{FF}(Q_p) should act
unitarily (eigenvalues on the unit circle) with respect to the canonical
metric. This would give the critical line.

**Why not automatic**: The Frobenius on the FF curve is a "dilatation" by p
(not a rotation). Proving it becomes unitary after the correct normalization
is the whole difficulty. It requires either:
- A delicate Hodge-theoretic argument (analogue of the Griffiths transversality
  that gives unitarity of the Hodge filtration), or
- An input from the arithmetic of the FF curve that is not yet understood

**Scholze's claim**: The canonical metric makes φ_p an isometry. But this
equally applies to all φ_p (for all primes), and the simultaneous unitarity
of infinitely many commuting operators has implications (e.g., the joint
spectrum lies on a torus iR^N) that need to be reconciled with the chaotic
distribution of primes.

**Status**: Open. This is the key claim that needs proof.

---

## 6. Archimedean Component / Twistor-P¹ Gap

**Statement**: The original FF curve exists only over p-adic fields. The
archimedean component requires a separate construction — Scholze proposed the
twistor-P¹ (P¹ over C with a certain C⁎-action).

**Developments**:
- Scholze (2024, IAS lectures): "Real local Langlands as geometric Langlands
  on the twistor-P¹" — connects the archimedean place to the twistor-P¹
- Anschütz-Bosco-LeBras-RodríguezCamargo-Scholze (2025, v2 2026): "Analytic
  de Rham stacks of Fargues-Fontaine curves" — 129 pages constructing analytic
  de Rham stacks and their relation to the FF curve

**Remaining issues**:
1. The twistor-P¹ approach is primarily about **local Langlands**, not RH.
   The connection to ζ(s) zeros is indirect.
2. The archimedean component must produce the Gamma factor Γ_R(s)⁷ (or similar)
   in the determinant identity. This has not been done.
3. The gluing of the p-adic FF curve(s) with the twistor-P¹ is not defined.
4. The user has dismissed this direction as "numerical approach, can't prove RH."

**Status**: The twistor-P¹ is the most active area of recent work, but it
addresses archimedean local Langlands, not the RH for ζ(s). The connection
remains speculative.

---

## 7. Shift 0 → ½ from Functional Equation

**Statement**: Even if Θ is proven skew-adjoint (Spec(Θ) ⊆ iR), this gives
det_∞(s-Θ) = ζ(s) with zeros at s = iγ, which are on Re(s) = 0, not
Re(s) = 1/2.

**Fix**: The complete ξ-function includes the Gamma factor and satisfies
ξ(s) = ξ(1-s). If we define Θ_total = Θ ⊕ Θ_∞, then:
- det_∞(s - ½ - Θ_total) = ξ(s)
- Spec(Θ_total) ⊆ iR ⇒ ξ(s)'s zeros are on Re(s) = ½

**Why this is a difficulty**: The shift by ½ is trivial algebraically but
requires a **justification for why Θ_total is the correct operator**. The
half-shift comes from the functional equation's symmetry, which in the
function field case arises from Serre duality / Poincaré duality. For the
FF curve over Spec Z, the analogue of Poincaré duality is not established.

**Status**: Minor difficulty compared to the others, but still unresolved.
The shift relies on a duality theory that doesn't yet exist for the FF curve
over Spec Z.

---

## 8. Comparison with Function Field Case Fails

**Statement**: The entire FF approach is modeled on the function field case
(curves C/F_q), where RH holds via Deligne's Weil II. The analogy is:

```
F_q[t]                ↔ Z
C/F_q (curve)         ↔ Spec Z (arithmetic curve)
ℓ-adic cohomology     ↔ FF curve cohomology (???)
Frobenius Frob_q      ↔ FF Frobenius φ_p (but which p?)
Weights = q^{w/2}    ↔ |eigenvalue| = ? (RH: Re(s)=½)
```

**Known obstructions to the analogy**:
1. Spec Z has "archimedean place" ∞; function field curves have only
   finite places.
2. The Frobenius for Spec Z is not canonical — there is no single Frobenius
   (the FF curve has per-prime Frobenius operators φ_p).
3. The function field RH reduces to bounding eigenvalues of a single
   operator. For Spec Z, we would need infinitely many commuting Frobenius
   operators with a simultaneous spectral bound.
4. The FF curve over Q_p is a curve over Q_p, not over Spec Z. Its
   cohomology is a p-adic cohomology, not a complex cohomology that could
   detect the critical line.

**Status**: The analogy is suggestive but breaks down at every key point.
The FF curve provides a geometric home for p-adic Hodge theory, not a
Weil cohomology for Spec Z.

---

## 9. Scholze's Construction is Unpublished

**Statement**: The FF approach to RH was announced in a 2023 MPIM talk.
No paper, preprint, or lecture notes exist. Everything is second-hand
(blog posts, listener notes).

**Consequences**:
- No details to verify, critique, or build upon
- Central claims ("canonical metric," "unitarity of Frobenius") cannot be
  checked
- The mathematical community has not vetted the approach
- The approach may have shifted (the 2024-2025 work focuses on the
  twistor-P¹ for local Langlands, not RH)

**Status**: The approach cannot be evaluated until a written document exists.
Given the user's time horizon, waiting for Scholze to publish is not an option.

---

## 10. WCart_HT(Z) ↔ Deninger's H^1_red: The Glue is Conjectural

**Statement**: The Sen-Weil operator construction (`sen_weil_complete_proof.md`,
`global_wcart_construction.md`) identifies:
- The global Sen operator Θ on WCart_HT(Z) with the generator of Deninger's
  R-action on W_rat(Spec Z)(C)
- The cohomology group H^1_red(WCart_HT(Z)) with H^1_red(W_rat(C))

This identification is the bridge between the prismatic (FF-adjacent) and
dynamical (Deninger) frameworks. But it is **conjectural**:
1. WCart_HT(Z) is defined via CRT fiber product — does it carry the same
   Hodge-Tate structure as the per-p components?
2. The equivalence of categories QCoh(WCart_HT(Z_p)) ≅ {complexes with Θ_p}
   is per-p. The global version requires a product of Sen operators acting on
   a completed tensor product — is this well-defined?
3. The identification with Deninger's H^1_red is at the level of C-points
   only. The cohomological equivalence is not proven.

**Status**: If this glue fails, the FF curve and the Deninger dynamical
system are unrelated objects, and the FF metric (even if it exists) says
nothing about Θ's spectrum.

---

## 11. No Weil Cohomology Axioms for Spec Z

**Statement**: The FF curve approach seeks to construct a Weil cohomology
for Spec Z (analogous to ℓ-adic cohomology for curves over F_q). But
Deninger (2022, arXiv:2204.02714) proved:

**Theorem (Deninger)**: There is no Weil cohomology theory with real
coefficients for arithmetic curves (including Spec Z).

**FF response**: The FF curve provides a **complex**-coefficient cohomology.
Deninger's theorem allows this.

**Remaining issue**: Even with complex coefficients, a Weil cohomology for
Spec Z must satisfy:
1. Finite dimensionality of H^i
2. Poincaré duality
3. Lefschetz trace formula
4. Purity / weight structure

The FF curve's cohomology (e.g., the cohomology of X_{FF}(Q_p)) does not
satisfy (1)-(4) for Spec Z — it is a cohomology of a curve over Q_p, not
a cohomology of Spec Z.

**Status**: The "complex-coefficient Weil cohomology for Spec Z" that the
FF approach requires does not exist and is not obviously provided by the
FF curve. Deninger's obstruction is evaded but the positive construction
remains missing.

---

## 12. Interaction with G5/G7 (Analytic Continuation + Continuous Trace)

**Statement**: The `remaining_gaps.md` identifies G5 and G7 as the most
fundamental gaps in the entire program. They are independent of the FF
framework.

- **G5**: ζ(s) non-trivial zeros are not eigenvalues of Θ. They come from
  analytic continuation of the Euler product.
- **G7**: The trace formula Tr(e^{tΘ}) = Σ log p·δ(t−log p) only captures
  the discrete part of the spectrum. The continuous spectrum (zeros) does
  not appear.

**Why the FF approach does not automatically resolve G5/G7**:
- The FF metric ensures Θ is skew-adjoint on L². But Θ's discrete spectrum
  is still {i·log p}. The continuous spectrum is still absent from the
  trace formula.
- The identity ζ(s) = det_∞(s-Θ) is an identity of analytic functions:
  both sides converge on Re(s)>1 and have analytic continuations. The
  zeros of ζ(s) are the **zeros of the analytic continuation** of the
  RHS's reciprocal, not eigenvalues of Θ.
- To make them eigenvalues, one would need a different operator (not the
  R-action generator) whose discrete spectrum is precisely the ζ zeros.
  The FF approach does not propose such an operator.

**Status**: G5/G7 are structural — they arise from the distinction between
"zeros of a zeta function" and "eigenvalues of an operator" that holds
for all Ruelle-type zeta functions. The FF metric does not bridge this gap
unless it provides an entirely new operator that bypasses the Deninger
trace formula.

---

## Summary Table

| # | Difficulty | Severity | Status |
|---|-----------|----------|--------|
| 1 | No global FF curve over Spec Z | Critical | Open |
| 2 | Canonical metric not constructed | Critical | Unpublished |
| 3 | Continuous spectrum / Ruelle obstruction | **Fatal** | Proved impossible (Ruelle Theorem) |
| 4 | Trace formula not derived from FF | Critical | Open |
| 5 | Unitarity of Frobenius not proven | Critical | Open |
| 6 | Archimedean / twistor-P¹ gap | Major | Active research (not RH-focused) |
| 7 | Shift 0→½ from functional equation | Minor | Resolvable in principle |
| 8 | Analogy to function fields fails | Major | Structural |
| 9 | Construction unpublished | Major | Cannot evaluate |
| 10 | WCart_HT(Z) ↔ Deninger glue conjectural | Major | Open |
| 11 | No Weil cohomology for Spec Z | Critical | Deninger evaded, construction missing |
| 12 | G5/G7 interaction (analytic continuation) | **Fatal** | Independent of metric |

**Key conclusion**: Difficulty 3 (Ruelle obstruction) and Difficulty 12
(G5/G7: analytic continuation zeros ≠ eigenvalues) are fatal. They prove
that **no operator** derived from the Deninger trace formula can prove RH,
regardless of metric. The FF approach would need to produce a fundamentally
different operator — not the R-action generator — whose discrete spectrum
equals the ζ zeros. The FF curve provides geometric language but does not
create new eigenvalues where none exist.

**The FF approach is not disproven** — it is possible that Scholze's
construction provides such a new operator via a completely different
mechanism (e.g., the Laplacian on the FF curve itself, not the R-action
generator). But until the construction is published, this remains
speculative, and the difficulties above (especially 1, 2, 4, 5, 11)
make it unlikely that a complete proof exists.
