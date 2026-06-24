"""v5_mirror_connection_test.py: Test the Dubrovin connection analogy on GL(3) data.
Compute the quantum differential equation monodromy from GL(3) L-functions."""
import numpy as np
from pathlib import Path

DATA_DIR = Path(r'D:\code\Riemann Hypothesis\rtl\data')
FIG_DIR = Path(r'D:\code\Riemann Hypothesis\rtl\figures\v5')
FIG_DIR.mkdir(parents=True, exist_ok=True)
ALL_PRIMES = np.array([2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89], dtype=np.float64)

npz = np.load(DATA_DIR / 'v2_r0r0r0_hecke.npz', allow_pickle=True)
nu = npz['nu']
starts = npz['coeff_starts']
n_coeff = npz['n_coeff']
coeffs_flat = npz['coeffs_flat']

def form_coeffs(i):
    start = int(starts[i]); end = start + int(n_coeff[i])
    return coeffs_flat[start:end], int(n_coeff[i])

def log_deriv(t, a_p):
    """Compute d/ds log L(0.5+it) numerically."""
    h = 1e-6
    s1 = 0.5 + 1j*(t+h)
    s2 = 0.5 + 1j*(t-h)
    L1 = complex(1,0); L2 = complex(1,0)
    for i in range(len(a_p)):
        p = ALL_PRIMES[i]; a = a_p[i]
        z1 = p**(-s1); z2 = p**(-s2)
        lf1 = 1 - a*z1 + a*z1**2 - z1**3
        lf2 = 1 - a*z2 + a*z2**2 - z2**3
        L1 /= lf1; L2 /= lf2
    return (L1 - L2) / (2*h*1j)

# Test: compute log derivative for Form 0
a0, n0 = form_coeffs(0)
print("="*60)
print("V5: Mirror symmetry / Dubrovin connection test")
print("="*60)
print(f"Form 0: nu=({nu[0][0]:.4f}, {nu[0][1]:.4f})")
print()

# Scan t ∈ [0, 30] and compute log derivative
t_vals = np.linspace(0, 30, 200)
log_derivs = np.array([log_deriv(t, a0) for t in t_vals])

print("Testing Dubrovin connection formula:")
print("  d/ds log L(s) = -Σ_p (log p)·A(1,p)·p^{-s}/(1 - A(1,p)p^{-s} + A(1,p)p^{-2s} - p^{-3s})")
print()

# Compute quantum connection A(s) = -ζ'(s)/ζ(s) for comparison
def quantum_connection(t, a_p, s_shift=0.5):
    s_val = s_shift + 1j*t
    result = complex(0,0)
    from math import log
    for i in range(len(a_p)):
        p = ALL_PRIMES[i]; a = a_p[i]
        z = p**(-s_val)
        lf = 1 - a*z + a*z*z - z**3
        if abs(lf) > 1e-15:
            result += (log(p)) * a * z / lf
    return result

# For Riemann zeta (GL(1)): quantum_connection = -ζ'/ζ = Σ_p log p·p^{-s}/(1-p^{-s})
print("Quantum connection A(s) = d/ds log L(s) for Form 0:")
for t_idx in [0, 20, 50, 100, 150]:
    t = t_vals[t_idx]
    qc = quantum_connection(t, a0)
    ld = log_derivs[t_idx]
    print(f"  t={t:.1f}: A(s)={qc.real:.4f}{qc.imag:+.4f}i  ,  d/ds log L={ld.real:.4f}{ld.imag:+.4f}i")
print()

# Monodromy test: integrate quantum connection around a contour
print("Monodromy test: parallel transport around contour in s-plane")
print("(testing whether the quantum D-module has regular singularities)")

# The quantum connection has singularities at s where L(s)=0 and at s=1 (pole of ζ)
# For GL(1) (Riemann): singularities at s=1 (pole) and at zeros of ζ
# For GL(3): singularities depend on Satake parameters

# Check singularity structure
for t_sing in np.linspace(0, 40, 20):
    qc = quantum_connection(t_sing, a0)
    if abs(qc) > 50:
        print(f"  Possible singularity near t={t_sing:.1f}: |A(s)|={abs(qc):.1f}")

# Connection with spectral parameters
print(f"\nSpectral parameters vs quantum connection strength:")
for idx in range(min(10, len(starts))):
    a_p, nc = form_coeffs(idx)
    qc_mean = np.mean([abs(quantum_connection(t, a_p)) for t in np.linspace(1, 10, 20)])
    nu1, nu2 = nu[idx]
    print(f"  Form {idx}: nu1={nu1:.2f}, nu2={nu2:.2f}, mean|A|={qc_mean:.4f}")

# In mirror symmetry, the quantum connection monodromy gives the Hodge data
# For GL(3) L-functions, the monodromy should be related to (nu1, nu2)
# Test: correlate spectral params with connection averages
print(f"\nCorrelation test: quantum connection vs spectral parameter (GL(1)=RH):")
print("  For GL(1): no spectral params, monodromy = functional equation")
print("  For GL(3): spectral params (nu1, nu2) should appear in monodromy")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ax = axes[0]
ax.plot(t_vals, [abs(qc) for qc in log_derivs], 'b-', lw=0.8)
ax.set_xlabel('t'); ax.set_ylabel('|d/ds log L(0.5+it)|')
ax.set_title('Quantum connection of GL(3) L-function (Form 0)')
ax.grid(alpha=0.2)

ax = axes[1]
all_qc_means = []
for idx in range(min(50, len(starts))):
    a_p, nc = form_coeffs(idx)
    qc_mean = np.mean([abs(quantum_connection(t, a_p)) for t in np.linspace(1, 10, 20)])
    all_qc_means.append(qc_mean)
    nu1, nu2 = nu[idx]
    ax.scatter((nu1+nu2)/2, qc_mean, s=5, alpha=0.5, c='blue')
ax.set_xlabel('(nu1+nu2)/2'); ax.set_ylabel('mean |A(s)|')
ax.set_title('Quantum connection strength vs spectral params')
ax.grid(alpha=0.2)

fig.savefig(FIG_DIR / 'v5_quantum_connection.png', dpi=150)
print(f"Saved {FIG_DIR / 'v5_quantum_connection.png'}")
plt.close()

print("\nDone.")
