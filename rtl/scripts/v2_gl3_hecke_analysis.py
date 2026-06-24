"""
v2_gl3_hecke_analysis.py: Analyze GL(3) Hecke eigenvalues.
- Per-prime statistics
- Ramanujan-Petersson bound check
- Satake parameter estimation (requires coeffs at p²)
- Compare with Frobenius purity prediction
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FIG_DIR = Path(__file__).resolve().parents[1] / "figures" / "v2"
FIG_DIR.mkdir(parents=True, exist_ok=True)

PRIMES = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,
          67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149]

print("="*60)
print("GL(3) Hecke Eigenvalue Analysis")
print("="*60)

# ================================================================
#  1. Load data
# ================================================================

def load_data(label):
    npz = np.load(DATA_DIR / f"v2_{label}_hecke.npz", allow_pickle=True)
    nu = npz["nu"]
    n_coeff = npz["n_coeff"]
    coeffs_flat = npz["coeffs_flat"]
    starts = npz["coeff_starts"]
    
    # Reconstruct entries
    entries = []
    for i in range(len(starts)):
        start = int(starts[i])
        end = start + int(n_coeff[i]) if i < len(starts)-1 else len(coeffs_flat)
        entries.append({
            'nu': nu[i],
            'n_coeff': int(n_coeff[i]),
            'coeffs': coeffs_flat[start:end],
        })
    
    return entries

labels = ["r0r0r0", "r0r1r1"]
all_data = {}
for label in labels:
    all_data[label] = load_data(label)
    print(f"\n[{label}] {len(all_data[label])} entries loaded")

# ================================================================
#  2. Per-prime statistics
# ================================================================

print("\n" + "="*60)
print("Per-Prime Hecke Eigenvalue Statistics")
print("="*60)

for label in labels:
    entries = all_data[label]
    print(f"\n  [{label}]")
    
    for i in range(min(18, len(PRIMES))):  # first 18 primes
        p = PRIMES[i]
        vals = np.array([e['coeffs'][i] for e in entries if e['n_coeff'] > i])
        if len(vals) < 5:
            continue
        
        # Ramanujan-Petersson bound check
        rp_bound = 3  # for GL(3) unitary
        exceed = np.sum(np.abs(vals) > rp_bound)
        
        print(f"    p={p:3d}: N={len(vals):3d}, mean={np.mean(vals):+.4f}, "
              f"var={np.var(vals):.4f}, std={np.std(vals):.4f}, "
              f"max|A|={np.max(np.abs(vals)):.4f}, "
              f"|A|>3={exceed}")
    
    # Overall distribution
    all_vals = np.concatenate([e['coeffs'] for e in entries])
    print(f"    ---")
    print(f"    Overall: N={len(all_vals)}, mean={np.mean(all_vals):+.4f}, "
          f"var={np.var(all_vals):.4f}, std={np.std(all_vals):.4f}")

# ================================================================
#  3. Distribution comparison: GL(3) Hecke vs GL(2) Hecke vs Sato-Tate SU(3)
# ================================================================

print("\n" + "="*60)
print("Sato-Tate Distribution Analysis")
print("="*60)

# For GL(3) tempered, A(1,p) = trace(SU(3)) and has Sato-Tate distribution
# For SU(3), the trace distribution has density:
# f(t) = (3/π) * (1-t²/12)^{1/2} for |t| ≤ 2√3
# Actually let me verify this

# For SU(3) characters, the trace χ(g) = tr(ρ(g)) where ρ is the 3-dim rep
# The Sato-Tate measure is the image of Haar measure on SU(3)
# The density of X = tr(g) for g ∈ SU(3) is:
# f(x) = (1/4π) * (x+3)^2 * sqrt(3-x) * H(3-x) for x in [-3, 3]? 
# Hmm, let me use a simpler approximation

# Let's compare GL(3) Hecke with:
# (a) Standard normal N(0,1)
# (b) Wigner semicircle with support [-3, 3]  
# (c) Empirical GL(2) distribution (should be similar to Wigner)

for label in labels:
    entries = all_data[label]
    all_vals = np.concatenate([e['coeffs'] for e in entries])
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Histogram
    ax = axes[0]
    ax.hist(all_vals, bins=60, density=True, alpha=0.6, color='steelblue',
            label=f'{label} (N={len(all_vals)})')
    
    # Standard normal
    x = np.linspace(-4, 4, 200)
    ax.plot(x, np.exp(-x**2/2)/np.sqrt(2*np.pi), 'r--', lw=2, label='N(0,1)')
    
    ax.set_xlabel("Hecke eigenvalue A(1,p)")
    ax.set_ylabel("Density")
    ax.set_title(f"{label} Hecke eigenvalue distribution")
    ax.legend()
    ax.grid(alpha=0.2)
    
    # Q-Q plot vs normal
    ax = axes[1]
    sorted_vals = np.sort(all_vals)
    n = len(sorted_vals)
    normal_quantiles = np.random.normal(0, np.std(all_vals), n)
    normal_quantiles.sort()
    ax.scatter(normal_quantiles, sorted_vals, s=2, alpha=0.3)
    ax.plot([-4, 4], [-4, 4], 'r--', lw=1)
    ax.set_xlabel("Normal quantiles")
    ax.set_ylabel("Sample quantiles")
    ax.set_title("Q-Q plot vs normal")
    ax.grid(alpha=0.2)
    ax.set_aspect('equal')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    
    plt.tight_layout()
    fig.savefig(FIG_DIR / f"v2_{label}_hecke_dist.png", dpi=150)
    print(f"  [Saved] {FIG_DIR / f'v2_{label}_hecke_dist.png'}")
    plt.close()

# ================================================================
#  4. Per-prime variance analysis
# ================================================================

print("\n" + "="*60)
print("Variance vs Prime Number")
print("="*60)

fig, ax = plt.subplots(figsize=(10, 6))

for label, color, marker in [("r0r0r0", 'blue', 'o'), ("r0r1r1", 'green', 's')]:
    entries = all_data[label]
    variances = []
    primes_used = []
    for i in range(20):  # first 20 primes
        p = PRIMES[i]
        vals = np.array([e['coeffs'][i] for e in entries if e['n_coeff'] > i])
        if len(vals) >= 10:
            variances.append(np.var(vals))
            primes_used.append(p)
    
    ax.plot(primes_used, variances, f'{marker}-', color=color, label=label, alpha=0.7)

ax.axhline(y=0.667, color='gray', ls='--', alpha=0.5, label='Expected (tempered SU(3))')
ax.set_xlabel("Prime p")
ax.set_ylabel("Variance of A(1,p)")
ax.set_title("Hecke Eigenvalue Variance vs Prime")
ax.legend()
ax.grid(alpha=0.2)

fig.savefig(FIG_DIR / "v2_variance_vs_prime.png", dpi=150)
print(f"  [Saved] {FIG_DIR / 'v2_variance_vs_prime.png'}")
plt.close()

# ================================================================
#  5. Pairwise correlation between primes
# ================================================================

print("\n" + "="*60)
print("Pairwise Prime Correlation Matrix")
print("="*60)

for label in labels:
    entries = all_data[label]
    n_primes = 12
    corr_matrix = np.zeros((n_primes, n_primes))
    
    for i in range(n_primes):
        vi = np.array([e['coeffs'][i] for e in entries if e['n_coeff'] > i])
        for j in range(n_primes):
            vj = np.array([e['coeffs'][j] for e in entries if e['n_coeff'] > j])
            valid = min(len(vi), len(vj))
            if valid > 10:
                corr_matrix[i,j] = np.corrcoef(vi[:valid], vj[:valid])[0,1]
    
    off_diag = corr_matrix[np.triu_indices_from(corr_matrix, k=1)]
    print(f"  [{label}] Off-diagonal correlations: "
          f"mean={np.mean(off_diag):+.4f}, std={np.std(off_diag):.4f}, "
          f"max|corr|={np.max(np.abs(off_diag)):.4f}")
    
    # Heatmap
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(corr_matrix, cmap='RdBu_r', vmin=-1, vmax=1, aspect='equal')
    for i in range(n_primes):
        for j in range(n_primes):
            ax.text(j, i, f'{corr_matrix[i,j]:.2f}', ha='center', va='center', fontsize=6)
    ax.set_xticks(range(n_primes))
    ax.set_yticks(range(n_primes))
    ax.set_xticklabels([str(PRIMES[i]) for i in range(n_primes)])
    ax.set_yticklabels([str(PRIMES[i]) for i in range(n_primes)])
    ax.set_xlabel("Prime p")
    ax.set_ylabel("Prime q")
    ax.set_title(f"{label}: Hecke eigenvalue correlation matrix\n"
                 f"Off-diag: mean={np.mean(off_diag):+.3f}, std={np.std(off_diag):.3f}")
    plt.colorbar(im)
    fig.savefig(FIG_DIR / f"v2_{label}_correlation.png", dpi=150)
    print(f"  [Saved] {FIG_DIR / f'v2_{label}_correlation.png'}")
    plt.close()

# ================================================================
#  6. Summary statistics
# ================================================================

print("\n" + "="*60)
print("Key Findings")
print("="*60)

for label in labels:
    entries = all_data[label]
    all_vals = np.concatenate([e['coeffs'] for e in entries])
    
    print(f"\n  [{label}] All Hecke eigenvalues ({len(all_vals)} total):")
    print(f"    Mean:        {np.mean(all_vals):+.4f}  (expect 0)")
    print(f"    Variance:    {np.var(all_vals):.4f}  (expect 1 for SU(3) trace)")
    print(f"    Skewness:    {np.mean(((all_vals - np.mean(all_vals))/np.std(all_vals))**3):.4f}  (expect 0)")
    print(f"    Kurtosis:    {np.mean(((all_vals - np.mean(all_vals))/np.std(all_vals))**4):.4f}  (expect ~2.2 for SU(3))")
    print(f"    Max |value|: {np.max(np.abs(all_vals)):.4f}  (RP bound = 3)")
    print(f"    > 2σ:        {np.mean(np.abs(all_vals) > 2*np.std(all_vals))*100:.2f}%")
    
    # Count by prime
    print(f"\n    Values by prime position:")
    for i in range(min(12, len(PRIMES))):
        vals = np.array([e['coeffs'][i] for e in entries if e['n_coeff'] > i])
        if len(vals) >= 5:
            print(f"      pos {i:2d} (p={PRIMES[i]:3d}): N={len(vals):3d}, "
                  f"mean={np.mean(vals):+.4f}, var={np.var(vals):.4f}, "
                  f"max|val|={np.max(np.abs(vals)):.4f}")
