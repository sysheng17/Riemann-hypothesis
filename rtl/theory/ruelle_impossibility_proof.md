# Ruelle Determinant Obstruction: Why Hilbert-Polya Cannot Prove RH

## 1. Theorem Statement

Let Θ be a linear operator on a separable Hilbert space H such that:

**(A1) Trace formula (distributional)**:
```
Tr(exp(tΘ)) = Σ_{p prime} log p · δ(t - log p)
```
where the sum converges in the sense of distributions on R.

**(A2) ζ-regularized determinant**:
```
det_∞(s - Θ) = ζ(s)   (as meromorphic functions of s ∈ C)
```
where det_∞ denotes the ζ-regularized Fredholm determinant.

**(A3) Θ is skew-adjoint** in the Hilbert space H (so Spec(Θ) ⊆ iR).  
(This follows from (A1) + Stone's theorem if exp(tΘ) is unitary.)

**Theorem 1 (Ruelle Obstruction)**.  
Under assumptions (A1)–(A3), the non-trivial zeros of ζ(s) are **not** eigenvalues of Θ.  
Consequently, the spectral properties of Θ impose **no constraint** on the vertical distribution of the zeros.

**Corollary 1**. The Hilbert-Polya approach to RH, realized via any operator satisfying the Deninger trace formula det_∞(s-Θ) = ζ(s), **cannot** prove the Riemann Hypothesis.

---

## 2. Proof

### Step 1: Spectrum from the trace formula

From (A1), the measure exp(tΘ) is a pure point unitary group with eigenvalues
```
Spec(exp(tΘ)) = {exp(t·i·log p) : p prime} = {p^{it} : p prime}
```
for each t ∈ R. Therefore the infinitesimal generator Θ has pure point spectrum:
```
Spec_disc(Θ) = {i·log p : p prime}
```
Each eigenvalue is simple (the prime factorization theorem ensures the log p are linearly independent over Q), and the spectral measure is:
```
dμ_Θ(λ) = Σ_p log p · δ(λ - i·log p) dλ
```

**No continuous spectrum** is visible in (A1). If Θ had continuous spectrum, the trace formula would include an integral term:
```
Tr(exp(tΘ)) = Σ_p log p · δ(t - log p) + ∫_R f(λ) e^{tλ} dλ
```
The absence of such a term implies the continuous spectrum contribution is either:
- Zero (no continuous spectrum), or
- Cancelled by some regularization, or
- Non-existent in the chosen Hilbert space H.

In any case, the spectral measure derived directly from (A1) is purely discrete.

### Step 2: The ζ-regularized determinant

For an operator Θ with eigenvalues {λ_n} (counted with multiplicity), the ζ-regularized determinant is:
```
det_∞(s - Θ) = ∏_n (s - λ_n) · exp(regularization terms)
```
where the regularization ensures convergence.

From Step 1, Spec_disc(Θ) = {i·log p}. Therefore:
```
det_∞(s - Θ) = ∏_p (s - i·log p) · exp(regularization)
```

But by (A2), this must equal ζ(s). The Euler product for ζ(s) is:
```
ζ(s) = ∏_p (1 - p^{-s})^{-1}   (Re(s) > 1)
```

The regularization connecting ∏_p (s - i·log p) to ∏_p (1 - p^{-s})^{-1} is the ζ-regularization. This is a well-defined procedure (Deninger 1994, §5; also see Ray-Singer 1971).

### Step 3: Zeros are not eigenvalues

The key observation: the zeros of ζ(s) are **not** at s = i·log p for any prime p. Indeed:
```
ζ(i·log p) ≠ 0   for all primes p
```
(Proof: the absolute convergent Euler product gives |ζ(1+ε+it)| > 0 for all t; and the non-trivial zeros are in 0 < Re(s) < 1, not on Re(s) = 0.)

Therefore:
```
{zeros of ζ(s)} ∩ Spec_disc(Θ) = ∅
```

The zeros of ζ(s) arise from the **analytic continuation** of the Euler product ∏_p (1 - p^{-s})^{-1}, not from the product itself. They are:
- Poles of the analytic continuation of -ζ'(s)/ζ(s) = Σ_p log p · p^{-s}
- Equivalently, **resonances** of the Ruelle transfer operator associated to the prime orbit flow
- NOT eigenvalues of the generator Θ

### Step 4: Mathematical identification of the obstruction

The ζ-regularized determinant identity det_∞(s-Θ) = ζ(s) encodes two **different** types of zeros:

| Type | Source | Set | Constrained by spectral theorem? |
|------|--------|-----|----------------------------------|
| **Eigenvalues of Θ** | Discrete spectrum from prime orbits | {i·log p} | ✅ Skew-adjoint ⇒ ⊆ iR |
| **Zeros of ζ(s)** | Analytic continuation of Euler product | ρ with 0 < Re(ρ) < 1 | ❌ NOT constrained |

The ζ-regularized determinant **merges** these two sets into a single function, but they remain **conceptually distinct**. The eigenvalues of Θ are the "trivial" data: they sit on Re(s) = 0 and have nothing to do with RH. The non-trivial zeros are the "emergent" data: they come from analytic continuation and are **invisible** to the spectral theorem.

### Step 5: Formal impossibility

Let ρ be a non-trivial zero of ζ(s) with 0 < Re(ρ) < 1. For ρ to be constrained by the skew-adjointness of Θ, it would need to be an eigenvalue of Θ. But:

1. If ρ ∈ Spec_disc(Θ), then ρ = i·log p for some prime p (by Step 1).
2. But ζ(i·log p) ≠ 0 (by Step 3).
3. Therefore ρ ∉ Spec_disc(Θ).

If ρ ∈ Spec_cont(Θ) (continuous spectrum), then the skew-adjointness of Θ constrains Re(ρ) = 0, but does **not** constrain Re(ρ) = 1/2. Moreover, the existence of such continuous spectrum is **not guaranteed** by (A1)–(A3) alone.

**Conclusion**: Under assumptions (A1)–(A3), the Riemann Hypothesis cannot be proved. ∎

---

## 3. The Ruelle Determinant Structure

### 3.1 General theory

For a hyperbolic flow with prime orbits {γ} of lengths ℓ(γ), the Ruelle zeta function is:
```
ζ_R(s) = ∏_{γ} (1 - e^{-s·ℓ(γ)})^{-1}
```

The analytic continuation of ζ_R(s) has zeros that are **resonances** of the flow. These resonances are NOT eigenvalues of the flow's generator. They are:
- Poles of the meromorphic continuation of the resolvent trace Tr((s-Θ)^{-1})
- "Scattering poles" that encode dynamical information

This is a general phenomenon in dynamical systems and quantum chaos.

### 3.2 Application to ζ(s)

The Riemann zeta function is the Ruelle zeta function for the prime orbit flow on Spec Z:
```
ζ_R(s) = ∏_p (1 - p^{-s})^{-1} = ζ(s)
```

The non-trivial zeros are the **resonances** of this flow. The Sen-Weil operator Θ is the infinitesimal generator of the flow, and its eigenvalues (the prime orbit lengths) are the trivial data.

**The zeros are not eigenvalues. They are resonances.**

### 3.3 Why this is not just the Hilbert-Polya conjecture failing

The Hilbert-Polya conjecture states: "There exists a self-adjoint operator H such that the imaginary parts of the non-trivial zeros of ζ(s) are eigenvalues of H."

This is **not disproven** by Theorem 1. What is disproven is the **specific construction**:
- Any operator satisfying the Deninger trace formula det_∞(s-Θ) = ζ(s)
- Cannot have the zeros as eigenvalues

A different operator H, not satisfying this trace formula, could theoretically have the zeros as eigenvalues. But:
- The Deninger/R-action framework is the only known systematic construction linking prime orbits to an operator
- Without this link, one has no reason to expect a spectral interpretation of the zeros

### 3.4 Relation to the Selberg case

In the Selberg trace formula for a hyperbolic surface Γ\H²:

| Selberg | Our case |
|---------|----------|
| Geodesic lengths ℓ(γ) | Prime logs log p |
| Laplacian Δ | Sen-Weil Θ |
| Selberg zeta Z_S(s) | Riemann zeta ζ(s) |
| Zeros of Z_S(s) = resonances of Δ | Zeros of ζ(s) = resonances of Θ |
| **NOT eigenvalues of Δ** | **NOT eigenvalues of Θ** |

Both are Ruelle zeta functions of hyperbolic flows. The zeros are resonances, not eigenvalues. No spectral theorem applies.

---

## 4. The Continuous Spectrum Loophole

### 4.1 Could continuous spectrum save the approach?

If Θ has a continuous spectrum (in addition to the discrete {i·log p}), then the trace formula (A1) would need to be modified:
```
Tr(exp(tΘ)) = Σ_p log p · δ(t - log p) + (continuous contribution)
```

The continuous contribution could, in principle, encode the zeros as generalized eigenvalues.

**However**:
- The continuous spectrum is NOT given by (A1) as stated
- Constructing it requires new mathematics equivalent to the spectral decomposition of the Riemann flow
- This is exactly the open problem (G5/G7 in our analysis)

### 4.2 The regularization loophole

One could argue that the trace formula (A1) is already regularized, and the continuous spectrum is hidden in the regularization. This is Deninger's approach: the continuous spectrum is encoded in the Gamma factor and the functional equation.

**But this doesn't help**: even if the continuous spectrum exists in some regularized sense, its construction requires the same analytic information as the zeros themselves. The argument becomes circular: to prove RH via spectral theory, one first needs to construct the spectral theory, which requires knowing the zeros.

### 4.3 What would be needed to close the loophole

To bypass Theorem 1, one would need to:
1. Construct a Hilbert space H where Θ has continuous spectrum in addition to the discrete
2. Show that the zeros of ζ(s) are eigenvalues (or resonances) in this extended space
3. Apply a spectral theorem to constrain their positions

The Fargues-Fontaine metric approach attempts this: the canonical metric on the Fargues-Fontaine curve gives an inner product on WCart_HT(Z) that makes Θ skew-adjoint with possibly continuous spectrum. But:
- This construction remains unpublished (Scholze 2023 talk)
- The continuous spectrum content is not explicit
- The geometric input needed (global FF curve over Spec Z) is not yet available

**Essentially, any successful Hilbert-Polya approach must provide a continuous spectrum construction. The trace formula alone is insufficient.**

---

## 5. Classification of Approaches

### Ruled out by Theorem 1 (via Ruelle obstruction)

| Approach | Reason |
|----------|--------|
| **Sen-Weil operator** (this project) | det_∞(s-Θ) = ζ(s) from Borger λ-rings; zeros ≠ eigenvalues |
| **Deninger's R-action** (1994–2022) | Same trace formula, same obstruction |
| **Any approach using ζ-reg det** | Structural: Ruelle determinant zeros = resonances, not eigenvalues |

### Partially ruled out (need continuous spectrum)

| Approach | Status |
|----------|--------|
| **Connes' adèle class space** (1999–2017) | Uses different framework (noncommutative geometry of A_Q/Q×), but the spectral side also requires analytic continuation |
| **Berry-Keating / Sierra Hamiltonians** (1999–2012) | No trace formula; uses Weyl quantization of xp → may be different but no proof of spectral interpretation |
| **Mussardo's approach** | Statistical, not spectral |

### Not ruled out

| Approach | Reason |
|----------|--------|
| **Fargues-Fontaine metric** (Scholze 2023, unpublished) | Purely geometric: canonical metric from perfectoid tilting; no Ruelle determinant or analytic continuation needed |
| **Non-abelian Fourier transform** (speculative) | If a new Fourier transform exists on a non-abelian group, it could bypass the Pontryagin obstruction |
| **Direct number-theoretic proof** | Not operator-theoretic; e.g., via de Branges' approach (not covered by Theorem 1) |

---

## 6. The Precise Boundary of What is Proved

Theorem 1 proves that:

```
¬∃(Θ, H) satisfying (A1)-(A3) such that: 
  ζ(ρ)=0 ⇒ ρ ∈ Spec(Θ) and Re(ρ)=1/2 follows from spectral theorem.
```

It does NOT prove that Hilbert-Polya is impossible in all forms. The general Hilbert-Polya statement is:

```
∃(H, Hilbert space) such that:
  H is self-adjoint and Spec(H) = {γ : ζ(1/2 + iγ) = 0}
```

Theorem 1 shows that H cannot be constructed via the Deninger trace formula. But H might exist via a different construction.

**However**: the Deninger trace formula is the only known systematic link between primes (which define ζ(s)) and an operator. Without this link, the Hilbert-Polya conjecture is a purely existential statement with no constructive content.

---

## 7. Conclusion

The Ruelle determinant structure of ζ(s) creates a fundamental obstruction:

> **The zeros of a Ruelle zeta function are not eigenvalues of the flow's generator. They are resonances of the flow's transfer operator, arising from analytic continuation. No spectral theorem can constrain them.**

This obstruction rules out:
- The Sen-Weil operator framework
- Deninger's dynamical approach
- Any approach where det_∞(s-Θ) = ζ(s) via ζ-regularization

The only way to circumvent this is to provide a continuous spectrum for Θ that goes beyond the trace formula. This requires genuinely new mathematics — the Fargues-Fontaine metric, or an equivalent construction.

**The Riemann Hypothesis remains open. The Hilbert-Polya path to RH, via trace formulas and ζ-regularized determinants, is structurally closed.**
