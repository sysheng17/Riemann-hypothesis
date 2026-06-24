"""Vectorized L-function scan, fixed for variable-length coeffs."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path(r'D:\code\Riemann Hypothesis\rtl\data')
FIG_DIR = Path(r'D:\code\Riemann Hypothesis\rtl\figures\v4');
FIG_DIR.mkdir(parents=True, exist_ok=True)

ALL_PRIMES = np.array([2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131], dtype=np.float64)

npz = np.load(DATA_DIR / 'v2_r0r0r0_hecke.npz', allow_pickle=True)
nu = npz['nu']
n_coeff = npz['n_coeff']
coeffs_flat = npz['coeffs_flat']
starts = npz['coeff_starts']
N_FORM = len(starts)
print(f"Forms: {N_FORM}, n_coeff range: [{np.min(n_coeff)}, {np.max(n_coeff)}]")

def form_coeffs(i):
    start = int(starts[i]); end = start + int(n_coeff[i])
    return coeffs_flat[start:end], int(n_coeff[i])

def L_at_t(t, a_p):
    """Compute L(0.5+it) for a single t, using all available coeffs."""
    s = 0.5 + 1j * t
    result = complex(1, 0)
    for i in range(len(a_p)):
        p = ALL_PRIMES[i]
        z = p ** (-s)
        a = a_p[i]
        lf = 1.0 - a*z + a*a*z*z - z**3
        result /= lf
    return result

def scan_form(form_idx, t_range=(0, 40), n_pts=500):
    a_p, _ = form_coeffs(form_idx)
    t_vals = np.linspace(t_range[0], t_range[1], n_pts)
    L_vals = np.array([L_at_t(t, a_p) for t in t_vals])
    absL = np.abs(L_vals)
    
    # Find dips (local minima below threshold)
    dips = []
    depth = []
    for j in range(1, len(t_vals)-1):
        if absL[j] < absL[j-1] and absL[j] < absL[j+1] and absL[j] < 0.5:
            dips.append(t_vals[j])
            depth.append(absL[j])
    
    return t_vals, absL, dips, depth

# =====================================================================
# Main scan: first 20 forms
# =====================================================================
n_scan = min(20, N_FORM)
fig, axes = plt.subplots(4, 5, figsize=(20, 12))
axes = axes.flatten()

all_dips = {}
for i in range(n_scan):
    t_vals, absL, dips, _ = scan_form(i, (0, 40), 500)
    all_dips[i] = dips
    
    ax = axes[i]
    ax.plot(t_vals, absL, 'b-', lw=0.6)
    ax.set_yscale('log')
    for d in dips:
        ax.axvline(x=d, color='r', ls='--', lw=0.4, alpha=0.4)
    ax.set_title(f"F{i}: nu=({nu[i][0]:.1f},{nu[i][1]:.1f}), {len(dips)} dips",
                 fontsize=9)
    ax.grid(alpha=0.2)

plt.tight_layout()
fig.savefig(FIG_DIR / 'v4_first20_scan.png', dpi=150)
print(f"Saved {FIG_DIR / 'v4_first20_scan.png'}")
plt.close()

# Statistics
dip_counts = [len(v) for v in all_dips.values()]
print(f"\nDip statistics (first {n_scan} forms):")
print(f"  Mean: {np.mean(dip_counts):.1f}, Std: {np.std(dip_counts):.1f}")
print(f"  Range: [{np.min(dip_counts)}, {np.max(dip_counts)}]")

# =====================================================================
# Form 0 detailed scan
# =====================================================================
a_p0, np0 = form_coeffs(0)
print(f"\nForm 0: {np0} primes")
print(f"  Primes used: {ALL_PRIMES[:np0].astype(int).tolist()}")

# Fine scan around dips
for t_center in [4, 12, 22]:
    t_fine = np.linspace(t_center - 0.5, t_center + 0.5, 200)
    L_fine = np.array([L_at_t(t, a_p0) for t in t_fine])
    absL_fine = np.abs(L_fine)
    min_idx = np.argmin(absL_fine)
    print(f"  Dip near t={t_center}: |L|={absL_fine[min_idx]:.6f} at t={t_fine[min_idx]:.4f}")

# Full plot
t_full = np.linspace(0, 60, 2000)
L_full = np.array([L_at_t(t, a_p0) for t in t_full])
absL_full = np.abs(L_full)

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(t_full, absL_full, 'b-', lw=0.7)
ax.set_yscale('log')
ax.set_xlabel('t'); ax.set_ylabel('|L(0.5 + it)|')
ax.set_title(f'Form 0: GL(3) approximate L-function, {np0} primes\n'
             f'nu=({nu[0][0]:.3f}, {nu[0][1]:.3f})')
ax.grid(alpha=0.2)

fig.savefig(FIG_DIR / 'v4_form0_full_L.png', dpi=150)
print(f"Saved {FIG_DIR / 'v4_form0_full_L.png'}")
plt.close()

# =====================================================================
# Compare: self-dual (A(p,1) = A(1,p)) vs trivial (A(p,1) = 0)
# =====================================================================
def L_at_t_no_dual(t, a_p):
    """Assume A(p,1) = 0 (wrong, but as baseline)."""
    s = 0.5 + 1j * t
    result = complex(1, 0)
    for i in range(len(a_p)):
        p = ALL_PRIMES[i]; z = p ** (-s); a = a_p[i]
        lf = 1.0 - a*z + 0*z*z - z**3
        result /= lf
    return result

t_test = np.linspace(0, 40, 200)
L_self = np.array([L_at_t(t, a_p0) for t in t_test])
L_no = np.array([L_at_t_no_dual(t, a_p0) for t in t_test])

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(t_test, np.abs(L_self), 'b-', lw=0.7, label='self-dual (A(p,1)=A(1,p))')
ax.plot(t_test, np.abs(L_no), 'r--', lw=0.7, label='trivial (A(p,1)=0)')
ax.set_yscale('log')
ax.legend(); ax.grid(alpha=0.2)
ax.set_xlabel('t'); ax.set_ylabel('|L(0.5+it)|')
ax.set_title('Self-dual vs trivial assumption')

fig.savefig(FIG_DIR / 'v4_dual_vs_trivial.png', dpi=150)
print(f"Saved {FIG_DIR / 'v4_dual_vs_trivial.png'}")
plt.close()

print("\nDone.")
