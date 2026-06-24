"""
v0: Finite Field Riemann Hypothesis - Prototype
Using an elliptic curve (g=1) over F_11 for simplicity.
RH = Hasse's theorem: |a1| <= 2*sqrt(q) is straightforward.
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

FIG_DIR = Path(__file__).resolve().parents[1] / "figures" / "v0"
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ================================================================
#  Curve: E: y^2 = x^3 + x + 1 over F_11 (elliptic, genus 1)
# ================================================================
p = 11
g = 1
a, b = 1, 1
print("=" * 60)
print(f"Elliptic curve: y^2 = x^3 + {a}x + {b} over F_{{{p}}}")

# Count points over F_p (naive enumeration)
count = 0
for x in range(p):
    rhs = (x**3 + a*x + b) % p
    if rhs == 0:
        count += 1
    else:
        # Euler criterion: is rhs a quadratic residue?
        legendre = pow(rhs, (p - 1) // 2, p)
        if legendre == 1:
            count += 2
count += 1  # point at infinity
a1 = count - (p + 1)  # #E = p + 1 - a1 (so a1 = -(trace of Frobenius))
print(f"  #E(F_{{{p}}}) = {count}  -> a1 = {a1}")

# RH for elliptic curves: |a1| <= 2*sqrt(p)
sqrt_p = np.sqrt(p)
rh_check = abs(a1) <= 2 * sqrt_p
print(f"  Hasse bound: |a1|={abs(a1)} <= 2*sqrt(p)={2*sqrt_p:.2f}  [{'RH OK' if rh_check else 'FAIL'}']")

# Frobenius eigenvalues: alpha, beta, with alpha+beta = a1, alpha*beta = p
# Compute from quadratic: T^2 - a1*T + p = 0  (since P_1(T) = 1 - a1*T + p*T^2)
discriminant = a1**2 - 4*p
alpha1 = (a1 + np.sqrt(complex(discriminant, 0))) / 2
alpha2 = (a1 - np.sqrt(complex(discriminant, 0))) / 2

print(f"  Frobenius eigenvalues:")
for j, alpha in enumerate([alpha1, alpha2], 1):
    mod = abs(alpha)
    print(f"    alpha_{j} = {alpha.real:.4f} + {alpha.imag:.4f}i  |alpha|={mod:.4f}  "
          f"(expected sqrt(p)={sqrt_p:.4f})  [{'RH OK' if abs(mod - sqrt_p) < 0.001 else 'FAIL'}]")

# ================================================================
#  Visualize
# ================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Circle plot
ax = axes[0]
theta = np.linspace(0, 2*np.pi, 400)
ax.plot(sqrt_p*np.cos(theta), sqrt_p*np.sin(theta), 'k--', lw=1, alpha=0.5, label=f'|z|={sqrt_p:.2f}')
ax.axhline(0, color='gray', lw=0.5)
ax.axvline(0, color='gray', lw=0.5)
for j, alpha in enumerate([alpha1, alpha2], 1):
    ax.plot(alpha.real, alpha.imag, 'ro', ms=10)
    ax.annotate(f'α{j}', (alpha.real, alpha.imag), xytext=(5, 5), textcoords='offset points')
ax.set_xlim(-sqrt_p-1, sqrt_p+1)
ax.set_ylim(-sqrt_p-1, sqrt_p+1)
ax.set_aspect('equal')
ax.set_xlabel('Re(α)'); ax.set_ylabel('Im(α)')
ax.set_title(f'Frobenius Eigenvalues (|α| = √{p} = {sqrt_p:.2f})')
ax.legend(); ax.grid(alpha=0.2)

# GL_n interpretation
ax = axes[1]
ax.axis('off')
lines = [
    f"RH for curves over F_q is PROVEN (Weil, 1949)",
    f"",
    f"E: y^2 = x^3 + {a}x + {b} over F_{{{p}}}",
    f"#E(F_{{{p}}}) = {count}",
    f"a1 = {a1} (trace of Frobenius)",
    f"|a1| = {abs(a1)} <= 2*√{p} = {2*sqrt_p:.2f}  [{('RH OK' if rh_check else 'FAIL')}]",
    f"",
    f"For elliptic curves:",
    f"  P_1(T) = 1 - a1*T + p*T^2",
    f"  Proves Hasse's theorem",
    f"",
    f"For higher genus curves:",
    f"  P_1(T) = det(1 - Frob·T | H¹_ét)",
    f"  Deligne's theorem: |α_j| = q^(1/2)",
    f"",
    f"Bun_GL_n analogue:",
    f"  P_1(T) = Tr(Frob* | IC(Bun_GL_n))",
    f"  Pure of weight n/2"
]
for i, line in enumerate(lines):
    ax.text(0.05, 0.95 - i*0.045, line, fontsize=11, fontfamily='monospace',
            verticalalignment='top')

plt.tight_layout()
fig.savefig(FIG_DIR / "v0_elliptic_rh_proven.png", dpi=150)
print(f"\n[Saved] {FIG_DIR / 'v0_elliptic_rh_proven.png'}")

# ================================================================
#  Save data
# ================================================================
results = {
    "curve": f"y^2 = x^3 + {a}x + {b}",
    "field": p,
    "genus": g,
    "point_count": count,
    "a1": a1,
    "rh_satisfied": bool(rh_check),
    "alpha1": complex(alpha1),
    "alpha2": complex(alpha2),
}
np.savez(DATA_DIR / "v0_results.npz", **results)
print(f"[Saved] {DATA_DIR / 'v0_results.npz'}")
print(f"\n{'='*60}")
print(f"KEY: Over F_q, RH is PROVEN (Weil, Deligne).")
print(f"The GL_n framework reinterprets this as")
print(f"purity of Hecke eigensheaves on Bun_GL_n(C).")
print(f"For Spec Z, the same purity is unproven.")
print(f"{'='*60}")
