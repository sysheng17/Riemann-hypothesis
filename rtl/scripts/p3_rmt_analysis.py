"""
RTL - P3: Random Matrix Analysis of Riemann Zeros
Compare normalized spacing against GOE / GUE / GSE ensembles
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import ks_1samp
from scipy.special import erf, gammainc
import time

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FIG_DIR  = Path(__file__).resolve().parents[1] / "figures" / "p3"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# -- Load zeros --
print("[P3] Loading zeros ...")
t_full = np.loadtxt(DATA_DIR / "zeros_odlyzko_100k.txt")
t_vals = t_full[:]
N = len(t_vals)
print(f"[P3] Using first {N:,} zeros")

# -- Normalized spacings --
gaps = np.diff(t_vals)
t_mid = (t_vals[:-1] + t_vals[1:]) / 2
mean_spacing = 2 * np.pi / np.log(t_mid / (2 * np.pi))
s = gaps / mean_spacing
print(f"[P3] Mean normalized spacing = {np.mean(s):.6f}")

# -- RMT distributions --
# GOE (beta=1): P(s) = (pi*s/2) * exp(-pi*s^2/4)
# GUE (beta=2): P(s) = (32/pi^2) * s^2 * exp(-4*s^2/pi)
# GSE (beta=4): P(s) = (262144/(729*pi^3)) * s^4 * exp(-64*s^2/(9*pi))

def goe_cdf(x):
    return 1 - np.exp(-np.pi * x**2 / 4)

def gue_cdf(x):
    return erf(2 * x / np.sqrt(np.pi)) - (4 * x / np.pi) * np.exp(-4 * x**2 / np.pi)

def gse_cdf(x):
    b = 64 / (9 * np.pi)
    return gammainc(2.5, b * x**2)

def goe_pdf(x):
    return (np.pi * x / 2) * np.exp(-np.pi * x**2 / 4)

def gue_pdf(x):
    return (32 / np.pi**2) * x**2 * np.exp(-4 * x**2 / np.pi)

def gse_pdf(x):
    return (262144 / (729 * np.pi**3)) * x**4 * np.exp(-64 * x**2 / (9 * np.pi))

# -- KS test against all three ensembles --
print("\n[P3] KS test results:")
results = {}
for name, cdf in [("GOE (b=1)", goe_cdf), ("GUE (b=2)", gue_cdf), ("GSE (b=4)", gse_cdf)]:
    stat, pv = ks_1samp(s, cdf)
    results[name] = (stat, pv)
    print(f"  {name:12s}: KS={stat:.6f}  p={pv:.6e}")

best_name = min(results, key=lambda k: results[k][0])
print(f"\n[P3] Best fit: {best_name} (KS={results[best_name][0]:.6f})")

# -- Number Variance Sigma^2(L) --
print("\n[P3] Computing Number Variance Sigma^2(L) ...")
L_max = 50
L_vals = np.arange(1.0, L_max + 0.5, 1.0)

unfolded = np.concatenate([[0], np.cumsum(s)])
max_unfold = unfolded[-1]
sigma2 = []
for L in L_vals:
    step = max(L, 1.0)
    starts = np.arange(unfolded[0], max_unfold - L, step)
    left = np.searchsorted(unfolded, starts, side='left')
    right = np.searchsorted(unfolded, starts + L, side='right')
    counts = right - left
    sigma2.append(np.var(counts, ddof=1))
sigma2 = np.array(sigma2)

# Theoretical asymptotic forms (leading order)
gue_sigma2 = (1 / np.pi**2) * np.log(L_vals) + 0.344
goe_sigma2 = (2 / np.pi**2) * np.log(L_vals) + 0.44
poisson_sigma2 = L_vals

# -- Dyson-Mehta Delta_3 (numerical integration) --
print("[P3] Computing Delta_3(L) ...")
delta3 = np.zeros(len(L_vals))
for idx, L in enumerate(L_vals):
    parts = []
    step = max(L * 2, 2.0)
    starts = np.arange(unfolded[0], max_unfold - L, step)
    for x0 in starts:
        left = np.searchsorted(unfolded, x0, side='left')
        right = np.searchsorted(unfolded, x0 + L, side='right')
        evals = unfolded[left:right] - x0  # positions in [0, L]
        M = len(evals)
        if M < 2:
            continue
        # Evaluate N(x) = step function on fine grid (100 points per window)
        n_grid = 100
        xs = np.linspace(0, L, n_grid)
        N_vals = np.searchsorted(evals, xs, side='right')
        # Least squares fit A + B*x to N_vals
        X_mat = np.column_stack([np.ones(n_grid), xs])
        coeff = np.linalg.lstsq(X_mat, N_vals, rcond=None)[0]
        res = N_vals - (coeff[0] + coeff[1] * xs)
        parts.append(np.sum(res**2) * (xs[1] - xs[0]) / L)
    delta3[idx] = np.mean(parts) if parts else 0

gue_delta3 = (1 / np.pi**2) * np.log(L_vals) - 0.007
poisson_delta3 = L_vals / 15
# -- Plot --
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle(f"RTL-P3: Random Matrix Analysis of Riemann Zeros (N={N:,})", fontsize=14)

ax = axes[0, 0]
x_grid = np.linspace(0, 4, 400)
ax.hist(s, bins=120, density=True, alpha=0.6, color="steelblue", label="Data")
ax.plot(x_grid, goe_pdf(x_grid), "g--", lw=1.5, label="GOE (b=1)")
ax.plot(x_grid, gue_pdf(x_grid), "r-", lw=2, label="GUE (b=2)")
ax.plot(x_grid, gse_pdf(x_grid), "m--", lw=1.5, label="GSE (b=4)")
ax.set_xlabel("Normalized spacing s"); ax.set_ylabel("Probability density")
ax.set_title("Nearest-Neighbor Spacing Distribution")
ax.legend(fontsize=10); ax.grid(alpha=0.2)

ax = axes[0, 1]
names = list(results.keys())
ks_vals = [results[n][0] for n in names]
colors = ["green", "red", "magenta"]
ax.bar(names, ks_vals, color=colors, alpha=0.7)
ax.set_ylabel("KS statistic"); ax.set_title("Goodness of Fit (lower is better)")
ax.grid(alpha=0.2, axis="y")

ax = axes[1, 0]
ax.plot(L_vals, sigma2, "b-", lw=1.5, label=f"Data (N={N:,})")
ax.plot(L_vals, gue_sigma2, "r--", lw=1.5, label="GUE theory")
ax.plot(L_vals, goe_sigma2, "g--", lw=1.5, label="GOE theory")
ax.plot(L_vals, poisson_sigma2, "k:", lw=1, label="Poisson")
ax.set_xlabel("Interval length L"); ax.set_ylabel("Sigma^2(L)")
ax.set_title("Number Variance"); ax.legend(fontsize=9); ax.grid(alpha=0.2)
ax.set_xlim(0, L_max)

ax = axes[1, 1]
ax.plot(L_vals, delta3, "b-", lw=1.5, label=f"Data (N={N:,})")
ax.plot(L_vals, gue_delta3, "r--", lw=1.5, label="GUE theory")
ax.plot(L_vals, poisson_delta3, "k:", lw=1, alpha=0.7, label="Poisson")
ax.set_xlabel("Interval length L"); ax.set_ylabel("Delta_3(L)")
ax.set_title("Dyson-Mehta Spectral Rigidity"); ax.legend(fontsize=9); ax.grid(alpha=0.2)
ax.set_xlim(0, L_max)

plt.tight_layout()
fig.savefig(FIG_DIR / "p3_rmt_analysis.png", dpi=150)
print(f"[P3] Figure saved: {FIG_DIR / 'p3_rmt_analysis.png'}")
plt.close()

# -- Output conclusion --
print(f"\n[P3] ===== CONCLUSION =====")
print(f"  Best fit: {best_name}")
print(f"  KS(GOE)={results['GOE (b=1)'][0]:.5f}")
print(f"  KS(GUE)={results['GUE (b=2)'][0]:.5f}")
print(f"  KS(GSE)={results['GSE (b=4)'][0]:.5f}")
print(f"  Sigma^2(L=10)={sigma2[19]:.4f} (GUE theory={gue_sigma2[19]:.4f})")
print(f"  Delta_3(L=10)={delta3[19]:.4f} (GUE theory={gue_delta3[19]:.4f})")

np.savez(DATA_DIR / "p3_results.npz",
         L_vals=L_vals, sigma2=sigma2, delta3=delta3,
         gue_sigma2=gue_sigma2, goe_sigma2=goe_sigma2, poisson_sigma2=poisson_sigma2,
         gue_delta3=gue_delta3, poisson_delta3=poisson_delta3,
         ks_goe=results['GOE (b=1)'][0],
         ks_gue=results['GUE (b=2)'][0],
         ks_gse=results['GSE (b=4)'][0])
print(f"[P3] Data saved to {DATA_DIR / 'p3_results.npz'}")
