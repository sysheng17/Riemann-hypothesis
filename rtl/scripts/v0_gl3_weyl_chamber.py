"""
v0: GL(3) Weyl Chamber Visualization
Shows why Sym^2 lift (1D curve) is insufficient for GL(3) generic spectrum.
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

FIG_DIR = Path(__file__).resolve().parents[1] / "figures" / "v0"
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
#  1. Load GL(2) data for Sym^2 lift
# ============================================================
print("[v0] Loading GL(2) Maass data ...")
maass_r = []
with open(DATA_DIR / "MaassForms.txt") as f:
    for line in f:
        parts = line.strip().split(":")
        if parts[0].startswith("1."):
            maass_r.append(float(parts[2]))
maass_r = np.array(maass_r)

# Sym^2 lift: (nu1, nu2, nu3) = (2R, 0, -2R)
# In 2D projection: (nu1, nu2) = (2R, 0) i.e., a line
sym2_nu1 = 2 * maass_r
sym2_nu2 = np.zeros_like(maass_r)

print(f"  {len(maass_r)} forms, R range: [{maass_r[0]:.1f}, {maass_r[-1]:.1f}]")

# ============================================================
#  2. Generate synthetic generic GL(3) points
# ============================================================
# Generic GL(3) principal series: (nu1, nu2, nu3) with nu1+nu2+nu3=0
# Weyl chamber: nu1 >= nu2 >= nu3 (after ordering)
# For our plot, we use (nu1, nu2) as coordinates, since nu3 = -nu1-nu2
# 
# The Weyl chamber boundary: nu1 >= nu2 >= -nu1-nu2
# This gives: nu2 >= 0 (since nu2 >= -nu1-nu2 => 2nu2 >= -nu1)
#             and nu1 >= nu2 (explicit)
# Also: nu1 + nu2 >= 0 (since nu3 = -nu1-nu2 <= nu2)

# Actually, for the spherical principal series with real spectral parameters:
# After Weyl ordering: nu1 >= nu2 >= nu3
# Conditions: nu1 >= nu2 >= 0  (since nu3 <= nu2 and nu1+nu2+nu3=0)

# Let me use a simpler model: points (nu1, nu2) with nu1 >= nu2 >= 0
# and a spectral cutoff nu1^2 + nu2^2 + nu1*nu2 <= R_cut^2

# Use the Weyl law: GL(3) spectral density
# Number of forms with spectral radius <= T is ~ T^5
# So we distribute points roughly proportional to this

np.random.seed(42)
n_generic = 5000  # enough for visualization

# Sample uniformly in the Weyl chamber with appropriate density
# We want the spectral density ~ T^5, so in polar coords, ~ r^4
# Simple approach: sample r^(1/5) uniformly, then angle uniformly
r_samples = np.random.uniform(0, 200, n_generic) ** (1/5) * 200
theta_samples = np.random.uniform(0, np.pi/4, n_generic)

# Map to (nu1, nu2) in the chamber nu1 >= nu2 >= 0
gen_nu1 = r_samples * np.cos(theta_samples)
gen_nu2 = r_samples * np.sin(theta_samples)

# Ensure ordering: nu1 >= nu2
mask = gen_nu1 >= gen_nu2
gen_nu1 = gen_nu1[mask]
gen_nu2 = gen_nu2[mask]

print(f"  Generated {len(gen_nu1)} generic GL(3) spectral points")

# ============================================================
#  3. Riemann zeros for comparison
# ============================================================
print("\n[v0] Loading Riemann zeros ...")
t_vals = np.loadtxt(DATA_DIR / "zeros_odlyzko_100k.txt")[:len(maass_r)]

# ============================================================
#  4. Visualization
# ============================================================

# (a) Weyl chamber: Sym^2 vs generic
fig = plt.figure(figsize=(16, 7))

ax = fig.add_subplot(1, 2, 1)
ax.scatter(sym2_nu1[:200], sym2_nu2[:200], s=8, c='red', alpha=0.6, label='Sym² lift (type B)')
ax.axhline(y=0, color='red', lw=2, alpha=0.3)
ax.set_xlabel("ν₁"); ax.set_ylabel("ν₂")
ax.set_title("GL(3) Sym² Lift Parameters\n(1D curve: ν₂=0, measure zero)")
ax.grid(alpha=0.2)
ax.legend()

ax = fig.add_subplot(1, 2, 2)
ax.scatter(gen_nu1[:2000], gen_nu2[:2000], s=3, c='blue', alpha=0.4, label='Generic GL(3) (type A)')
ax.scatter(sym2_nu1[:200], sym2_nu2[:200], s=8, c='red', alpha=0.8, label='Sym² lift (type B)')
ax.set_xlabel("ν₁"); ax.set_ylabel("ν₂")
ax.set_title("GL(3) Weyl Chamber\n(2D area vs 1D curve)")
ax.set_xlim(0, 300); ax.set_ylim(0, 200)
ax.grid(alpha=0.2)
ax.legend()

plt.tight_layout()
fig.savefig(FIG_DIR / "v0_gl3_weyl_chamber.png", dpi=150)
print(f"[Saved] {FIG_DIR / 'v0_gl3_weyl_chamber.png'}")
plt.close()

# (b) 3D Weyl chamber
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(111, projection='3d')

# Sym^2 points: (nu1, nu2, nu3) = (2R, 0, -2R) -> lie on a line
sym2_nu3 = -sym2_nu1 - sym2_nu2
ax.scatter(sym2_nu1[:100], sym2_nu2[:100], sym2_nu3[:100],
           c='red', s=10, alpha=0.7, label='Sym² lift (ν₂=0 line)')

# Generic points
gen_nu3 = -gen_nu1 - gen_nu2
ax.scatter(gen_nu1[:300], gen_nu2[:300], gen_nu3[:300],
           c='blue', s=3, alpha=0.3, label='Generic GL(3)')

ax.set_xlabel("ν₁"); ax.set_ylabel("ν₂"); ax.set_zlabel("ν₃")
ax.set_title("GL(3) Langlands Parameters (ν₁+ν₂+ν₃=0)")
ax.legend(fontsize=9)

fig.savefig(FIG_DIR / "v0_gl3_weyl_3d.png", dpi=150)
print(f"[Saved] {FIG_DIR / 'v0_gl3_weyl_3d.png'}")
plt.close()

# (c) Spectral density comparison
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# GL(2) density
ax = axes[0]
ax.hist(maass_r, bins=50, density=True, alpha=0.6, color='blue')
ax.set_title(f"GL(2) R density (n={len(maass_r)})")
ax.set_xlabel("Spectral parameter R"); ax.set_ylabel("Density")

# GL(3) Sym^2 density (rescaled)
ax = axes[1]
ax.hist(sym2_nu1, bins=50, density=True, alpha=0.6, color='red')
ax.set_title(f"GL(3) Sym²: 2R density (n={len(maass_r)})")
ax.set_xlabel("2R (spectral param)"); ax.set_ylabel("Density")

# Generic GL(3) density
ax = axes[2]
r_gen = np.sqrt(gen_nu1**2 + gen_nu2**2 + gen_nu1*gen_nu2)
ax.hist(r_gen[:len(maass_r)], bins=50, density=True, alpha=0.6, color='purple')
ax.set_title("Generic GL(3) spectral radius density")
ax.set_xlabel("|ν|"); ax.set_ylabel("Density")

plt.tight_layout()
fig.savefig(FIG_DIR / "v0_gl3_density_comparison.png", dpi=150)
print(f"[Saved] {FIG_DIR / 'v0_gl3_density_comparison.png'}")
plt.close()

# ============================================================
#  5. Summary
# ============================================================
print(f"""
{'='*60}
GL(3) Weyl Chamber Analysis
{'='*60}

The Sym^2 lift gives GL(3) parameters (2R, 0, -2R):
  - These lie on a line in the 2D Weyl chamber
  - ν₂ = 0 always → 1-dimensional subset
  - This is measure zero in the full GL(3) spectrum

Generic GL(3) principal series fills the 2D chamber:
  ν₁ ≥ ν₂ ≥ -ν₁-ν₂ = ν₃
  The counting function: N(T) ~ T^5

Key insight:
  ζ zeros are 'everywhere' in the n→∞ sense.
  Sym^2 lifts are 'nowhere' in the GL(3) spectrum.
  To understand the transition, we need generic GL(3) data.
""")
