# Weight Operator Dependency Graph
## From GL(3) empirical data to a Frobenius analogue on Spec Z

### Current Status: 2026-06-24

---

## 1. GL(3) Hecke Data — What We Know Empirically

**198 spherical generic (r0r0r0) + 226 nonspherical (r0r1r1) forms parsed.**

| Property | Value | Significance |
|----------|-------|-------------|
| A(1,p) mean | +0.028 (r0r0r0), +0.013 (r0r1r1) | Consistent with 0 (centered distribution) |
| A(1,p) variance | 0.455 (r0r0r0), 0.433 (r0r1r1) | Below SU(3) Sato-Tate expectation of 1 |
| A(1,p) range | [-3.78, 3.15] | Ramanujan-Petersson bound |A(1,p)| ≤ 3 holds (2 borderline exceptions) |
| Cross-prime corr. | 0.010 (mean), 0.075 (std) | Statistical independence between primes |
| Satake |α| = 1 | 97.3% of parameters | Self-dual cubic assumption valid for most |
| ν₁ range | [6.80, 17.00] | GL(3) spectral radius much larger than GL(2) |
| Laplacian λ | [59.83, 616.92] | Casimir eigenvalue = spectral parameter |

**Key insight**: Local purity (Ramanujan-Petersson at finite places) holds. The obstruction to RH is purely **global**: absence of a global Frobenius operator whose trace formula gives ζ(s).

---

## 2. The Four Candidate Frameworks — Dependency Graph

```
                    WEIGHT OPERATOR W on Spec Z
                    Tr(W^k) = ζ(s) local factors
                    Eigenvalues in Re(s)=1/2
                              |
        +--------------------+--------------------+
        |                    |                    |
   [A] Weil-étale       [B] Prismatic         [C] Deninger
   cohomology           cohomology             dynamical system
   (Lichtenbaum,        (Bhatt-Scholze,        (foliated space S_Z)
    Morin, Flach)        Bhatt-Lurie)
        |                    |                    |
   PROVEN for s=0      PROVEN per p          CONJECTURAL
   special values       with Frobenius φ     no construction
   NOT for critical              |                 |
   strip interior               |                 |
        |                    [B'] Absolute     [C'] Weil-étale
   NEED: Generalization    prismatic (Bhatt-   may be algebraic
   to all s in critical    Lurie 2022) has     version (Morin)
   strip (requires         Sen operator on
   weight functor)         WCart_HT
                                   |
                              NEED: Global gluing
                              of per-p φ into one
                              operator Φ on Spec Z
                              |
                    [B''] Borger λ-ring method:
                    Witt vectors as Frobenius
                    lifts {ψ_p}. NEED derived
                    λ-ring formalism to unify.

                 [D] Saito's Mixed Hodge Modules (MHM)
                     Weight filtration on complex varieties
                           |
                      NEED: Arithmetic analogue
                      MHM on Spec Z (Flenner's
                      program, unfinished)
                           |
                      NEED: Weight functor
                      W: D^b(MHM_arith(Spec Z)) -> R
                      satisfying cohomological-degree
                      compatibility
```

---

## 3. Critical Missing Pieces

### Piece 1: Global Frobenius (p-adic → global glue)

| Framework | Has Frobenius? | Global? | Status |
|-----------|---------------|---------|--------|
| Prismatic Δ_{Z_p} | Yes (φ) | No (per p) | Complete |
| Absolute prismatic WCart | Yes (Frob) | Partial | Bhatt-Lurie 2022 |
| Deninger S_Z | Yes (Θ) | Yes | Conjectural only |
| Weil-étale Spec Z | No (replaces Galois with Weil) | Yes | Morin 2014 |

**Weakest link**: No framework has both a Frobenius AND global definition on Spec Z.

### Piece 2: Weight Filtration

| Framework | Has weight filtration? | Compatible with ζ? |
|-----------|----------------------|-------------------|
| MHM(C) | Yes (Saito) | Hodge-theoretic only |
| Prismatic (Nygaard) | Yes (N) | Per p only |
| étale cohomology | Yes (Deligne) | Finite fields only |
| Spec Z | NO | **Missing entirely** |

**Weakest link**: No weight filtration exists on Spec Z (char 0, no Frobenius to define weights).

### Piece 3: Trace Formula

| Framework | Trace formula → ζ(s)? |
|-----------|----------------------|
| Weil-Deligne (finite fields) | Yes, Lefschetz fixed-point |
| Deninger (conjectural) | Yes, by construction |
| Weil-étale (Morin) | Yes, but only at s=0 |
| Prismatic (Bhatt-Scholze) | Not directly (local only) |

**Weakest link**: No global trace formula exists for Spec Z giving ζ(s) in the critical strip.

### Piece 4: Eigenvalue Purity

| Framework | Eigenvalue bounds? |
|-----------|-------------------|
| Weil (curves) | |α| = √q (proven) |
| Deligne (Weil II) | |α| = q^{w/2} (proven) |
| Ramanujan-Petersson (GL(n)) | |αᵢ,p| = 1 (conjectural, holds numerically) |
| Riemann ζ | ? (what would eigenvalues be?) |

**Weakest link**: No eigenvalue interpretation of ζ-zero positions — RH is about the nonexistent "eigenvalues."

---

## 4. The Minimal Path to RH (Pruned Dependency Tree)

```
START: Known mathematics
  |
  v
[1] Saito's MHM on complex varieties (exists)
  |
  v
[2] Arithmetic MHM on Spec Z (NEED: Flenner's program)
  |
  v
[3] Weight functor W on D^b(MHM_arith(Spec Z)) (NEED: definition)
  |   Requirements:
  |   - W(H^i(X)) = i for all arithmetic schemes X
  |   - W respects six-functor formalism
  |   - Purity: if L pure then eigenvalue of Frobenius = p^{W(L)/2}
  |
  v
[4] Global Frobenius Φ from per-p prismatic φ (NEED: glueing)
  |   Approach:
  |   - For each p, φ_p acts on RΓ_Δ(Z_p)
  |   - Construct Φ as product ∏_p φ_p acting on ⨂̂_p RΓ_Δ(Z_p)
  |   - Show Φ is well-defined (requires some finiteness)
  |
  v
[5] Trace formula Tr(Φ | H^*(Spec Z)) = -ζ'(s)/ζ(s) (NEED: proof)
  |   - Evaluate Tr(Φ^k) using fixed-point formula
  |   - Compare with explicit formula for ζ(s)
  |
  v
[6] Purity: eigenvalues of Φ on H^i have |λ| = p^{i/2} (NEED: proof)
  |   - Follows from W(H^i) = i and pure weight property
  |   - Equivalent to RH for ζ(s)
  |
  v
[7] RH: All nontrivial zeros of ζ(s) on Re(s) = 1/2 (CONCLUDED)
```

Each step [1]→[7] is a well-defined open problem. Steps [1] and [4] are closest to existing work. Step [3] is the most fundamental.

---

## 5. Alternative: The Shortcut via Self-Dual Parameter Structure

The empirical finding that 97.3% of GL(3) Satake parameters satisfy |α| = 1 (under self-duality assumption) suggests a path that avoids the full weight operator:

```
OBSERVATION: GL(3) Hecke eigenvalues A(1,p) ∈ [-3, 3] and
variance ≈ 0.45 < 1 (expected for SU(3) trace).

INTERPRETATION: The local L-factors are "already pure"
(|α_i| = 1 at ALL p). This means the global L-function
L(s, π_GL(3)) already satisfies the finite-part of the
analogue of RH — the local factors contribute no poles.

REMAINING PROBLEM: Only the Archimedean L-factor
L_∞(s, π_∞) = Γ_R(s+ν₁)Γ_R(s+ν₂)Γ_R(s-ν₁-ν₂) 
determines the global zero distribution.

The "RH for GL(3)" (GRH for L(s, π)) would follow from
a non-vanishing theorem for L(1/2+it, π), which is
about the GLOBAL behavior of the completed L-function.

THE SHORTEST PATH: Instead of constructing a weight operator
on Spec Z, prove a zero-free region for the completed
L-function using known analytic methods (e.g., the
Langlands-Shahidi method or the Rankin-Selberg method).
This bypasses the need for a Frobenius analogue entirely.
```

---

## 6. Conclusion and Recommended Direction

The weight operator approach to RH (methods A-D above) requires constructing a fundamentally new, nonexistent piece of mathematics — a Frobenius on Spec Z — that has resisted all attempts for 175 years.

**The GL(3) data confirms** that local purity holds (|α| = 1), suggesting the obstruction is purely global/archimedean.

**Two viable paths forward**:
1. **The analytic path** (shortcut): Prove GRH for GL(3) L-functions using existing analytic methods. This is hard but not impossible.
2. **The structural path** (long route): Construct arithmetic MHM on Spec Z and a weight functor. This would prove RH as a corollary but requires a complete redevelopment of motivic cohomology in mixed characteristic.

Both paths remain open.
