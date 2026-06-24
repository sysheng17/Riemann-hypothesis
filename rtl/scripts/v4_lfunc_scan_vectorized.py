"""Vectorized L-function scan for GL(3) Hecke data."""
import numpy as np
from pathlib import Path

DATA_DIR = Path(r'D:\code\Riemann Hypothesis\rtl\data')
FIG_DIR = Path(r'D:\code\Riemann Hypothesis\rtl\figures\v4')
FIG_DIR.mkdir(parents=True, exist_ok=True)

PRIMES = np.array([2,3,5,7,11,13,17,19,23,29,31,37], dtype=np.float64)

npz = np.load(DATA_DIR / 'v2_r0r0r0_hecke.npz', allow_pickle=True)
nu = npz['nu']
n_coeff = npz['n_coeff']
coeffs_flat = npz['coeffs_flat']
starts = npz['coeff_starts']

N_FORM = len(starts)
print(f"Forms: {N_FORM}, primes: {len(PRIMES)}")

def form_coeffs(i):
    start = int(starts[i])
    end = start + int(n_coeff[i])
    return coeffs_flat[start:end]

def vectorized_L(t_vals, a_p, primes):
    """Compute L(0.5+it) for all t in t_vals using vectorized ops."""
    n_t = len(t_vals)
    s = 0.5 + 1j * t_vals
    result = np.ones(n_t, dtype=np.complex128)
    n_p = len(a_p)
    for i in range(n_p):
        p = primes[i]
        z = p ** (-s)
        a = a_p[i]
        lf = 1.0 - a*z + a*a*z*z - z**3
        result /= lf
    return result

# Scan first 50 forms at fine grid
print("Scanning forms for zero candidates (t=0..40, 1000 pts)...")
t_scan = np.linspace(0, 40, 1000)

all_dips = []
n_forms_scan = min(50, N_FORM)
for i in range(n_forms_scan):
    a_p = form_coeffs(i)
    L = vectorized_L(t_scan, a_p)
    absL = np.abs(L)
    
    # Find local minima below threshold
    dips = []
    for j in range(1, len(t_scan)-1):
        if absL[j] < absL[j-1] and absL[j] < absL[j+1] and absL[j] < 0.5:
            dips.append(t_scan[j])
    
    # Cluster: if dips are within 0.5 of each other, keep the deepest
    if dips:
        clustered = [dips[0]]
        for d in dips[1:]:
            if d - clustered[-1] > 0.5:
                clustered.append(d)
        all_dips.append(clustered)

# Statistics
dip_counts = [len(d) for d in all_dips]
all_dip_vals = [d for sub in all_dips for d in sub]
print(f"\nZero candidates across {n_forms_scan} forms:")
print(f"  Mean candidates per form: {np.mean(dip_counts):.1f}")
print(f"  Total candidates: {len(all_dip_vals)}")
if all_dip_vals:
    print(f"  Candidate values: {np.round(np.sort(np.unique(np.round(all_dip_vals, 1))), 1)}")

# Spectral parameters regression
print(f"\nRegressing zero count vs spectral parameter:")
for i in range(n_forms_scan):
    nu1, nu2 = nu[i]
    print(f"  Form {i}: nu=({nu1:.2f},{nu2:.2f}), "
          f"zero candidates={len(all_dips[i])}")

# Check form 0 at t=4 (dip)
a_p0 = form_coeffs(0)
t_fine = np.linspace(3.5, 4.5, 100)
L_fine = vectorized_L(t_fine, a_p0)
absL_fine = np.abs(L_fine)
min_idx = np.argmin(absL_fine)
print(f"\nForm 0 dip near t=4: |L|={absL_fine[min_idx]:.6f} at t={t_fine[min_idx]:.4f}")

# Check form 0 at t=22
t_fine2 = np.linspace(21.5, 22.5, 100)
L_fine2 = vectorized_L(t_fine2, a_p0)
absL_fine2 = np.abs(L_fine2)
min_idx2 = np.argmin(absL_fine2)
print(f"Form 0 dip near t=22: |L|={absL_fine2[min_idx2]:.6f} at t={t_fine2[min_idx2]:.4f}")

# Plot form 0 L-function
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

t_full = np.linspace(0, 50, 2000)
L_full = vectorized_L(t_full, a_p0)
absL_full = np.abs(L_full)

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(t_full, absL_full, 'b-', lw=0.8)
ax.set_yscale('log')
ax.set_xlabel('t')
ax.set_ylabel('|L(0.5 + it)|')
ax.set_title(f'Form 0: GL(3) approximate L-function, 12 primes\n'
             f'nu=({nu[0][0]:.3f}, {nu[0][1]:.3f})')
ax.grid(alpha=0.2)

# Mark candidate zeros
for d in all_dips[0]:
    ax.axvline(x=d, color='r', ls='--', lw=0.5, alpha=0.5)

fig.savefig(FIG_DIR / 'v4_form0_L_function.png', dpi=150)
print(f"Saved {FIG_DIR / 'v4_form0_L_function.png'}")
plt.close()
