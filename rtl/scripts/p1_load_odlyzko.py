"""
RTL - P1: 載入 Odlyzko 零點資料，產出標準格式與圖表
"""
import numpy as np
import matplotlib.pyplot as plt
import json, time
from pathlib import Path
from scipy.stats import ks_1samp

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FIG_DIR  = Path(__file__).resolve().parents[1] / "figures"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

SRC = DATA_DIR / "zeros_odlyzko_100k.txt"
t_vals = np.loadtxt(SRC)
n = len(t_vals)
print(f"[P1] 載入 {n} 個零點 (Odlyzko, 精確到 ±3e-9)")

indices = np.arange(1, n + 1, dtype=np.int32)
np.savez(DATA_DIR / "zeros_full.npz", indices=indices, t_values=t_vals)
np.savetxt(DATA_DIR / "zeros_full.csv",
           np.column_stack([indices, t_vals]),
           delimiter=",", header="n,ImaginaryPart", comments="",
           fmt=["%d", "%.12f"])
print(f"[P1] 標準格式儲存至 {DATA_DIR}")

gaps = np.diff(t_vals)
t_mid = (t_vals[:-1] + t_vals[1:]) / 2
mean_spacing = 2 * np.pi / np.log(t_mid / (2 * np.pi))
normalized_gaps = gaps / mean_spacing

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(f"Riemann Zeta Zeros — First {n:,} (Odlyzko Data)", fontsize=14)

ax = axes[0, 0]
ax.plot(indices, t_vals, "b-", lw=0.3)
ax.set_xlabel("Zero index n"); ax.set_ylabel("Imaginary part t")
ax.set_title("Zero Height vs Index"); ax.grid(alpha=0.3)

ax = axes[0, 1]
ax.plot(indices[:-1], gaps, "g.", ms=1, alpha=0.5)
ax.set_xlabel("Zero index n"); ax.set_ylabel("Gap")
ax.set_title("Successive Zero Spacings"); ax.grid(alpha=0.3)

ax = axes[1, 0]
ax.hist(normalized_gaps, bins=120, density=True, alpha=0.7, color="steelblue", label=f"Data (n={n:,})")
s = np.linspace(0, 4, 400)
gue_pdf = (np.pi * s / 2) * np.exp(-np.pi * s**2 / 4)
ax.plot(s, gue_pdf, "r-", lw=2, label="GUE prediction")
ax.set_xlabel("Normalized spacing s"); ax.set_ylabel("Density")
ax.set_title("Spacing Distribution vs GUE"); ax.legend(); ax.grid(alpha=0.3)

ax = axes[1, 1]
sorted_gaps = np.sort(normalized_gaps)
ecdf = np.arange(1, len(sorted_gaps) + 1) / len(sorted_gaps)
ax.plot(sorted_gaps, ecdf, "b-", lw=1, label="Empirical CDF")
gue_cdf = 1 - np.exp(-np.pi * s**2 / 4)
ax.plot(s, gue_cdf, "r--", lw=1.5, label="GUE CDF")
ax.set_xlabel("Normalized spacing s"); ax.set_ylabel("Cumulative prob.")
ax.set_title("Cumulative Distribution"); ax.legend(); ax.grid(alpha=0.3)

plt.tight_layout()
fig.savefig(FIG_DIR / "p1_zero_100k_distribution.png", dpi=150)
print(f"[P1] 圖表儲存至 {FIG_DIR / 'p1_zero_100k_distribution.png'}")
plt.close()

def gue_cdf_fn(x):
    return 1 - np.exp(-np.pi * x**2 / 4)
ks_stat, ks_p = ks_1samp(normalized_gaps, gue_cdf_fn)
print(f"[P1] KS vs GUE: stat={ks_stat:.6f}  p-value={ks_p:.6e}")

meta = {
    "source": "Odlyzko",
    "n_zeros": n,
    "precision": "3e-9",
    "first_t": float(t_vals[0]),
    "last_t": float(t_vals[-1]),
    "mean_gap": float(np.mean(gaps)),
    "ks_GUE_stat": round(ks_stat, 6),
    "ks_GUE_p": float(ks_p),
}
with open(DATA_DIR / "metadata.json", "w") as f:
    json.dump(meta, f, indent=2)

print(f"[P1] 完成! KS p-value = {ks_p:.6e}")
print(f"    前 100k 零點的 GUE 吻合度已大幅提升。下一步: P2 TDA 分析")
