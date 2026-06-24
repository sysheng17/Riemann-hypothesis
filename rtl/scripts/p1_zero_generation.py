"""
RTL - P1: 黎曼 ζ 零點數據生成與基礎分析
"""
import mpmath as mp
import numpy as np
import matplotlib.pyplot as plt
import json, time, sys
from pathlib import Path
from scipy.stats import ks_1samp

MP_DPS = 30
N_ZEROS = 1_000
BATCH_LOG = 100
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FIG_DIR  = Path(__file__).resolve().parents[1] / "figures"
DATA_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)

mp.mp.dps = MP_DPS

print(f"[P1] 計算前 {N_ZEROS} 個非平凡零點 (dps={MP_DPS})", flush=True)
t0 = time.time()
t_values = np.empty(N_ZEROS, dtype=np.float64)

for i in range(1, N_ZEROS + 1):
    z = mp.zetazero(i)
    t_values[i - 1] = float(mp.im(z))
    if i % BATCH_LOG == 0:
        elapsed = time.time() - t0
        rate = i / elapsed
        eta = (N_ZEROS - i) / rate if rate > 0 else 0
        print(f"  [{i}/{N_ZEROS}]  t={t_values[i-1]:.3f}  "
              f"{rate:.0f} z/s  ETA={eta:.0f}s", flush=True)

elapsed = time.time() - t0
print(f"[P1] 完成! {N_ZEROS} zeros in {elapsed:.1f}s ({N_ZEROS/elapsed:.0f} z/s)", flush=True)

# 儲存
indices = np.arange(1, N_ZEROS + 1, dtype=np.int32)
np.savez(DATA_DIR / "zeros_full.npz", indices=indices, t_values=t_values)
np.savetxt(DATA_DIR / "zeros_full.csv",
           np.column_stack([indices, t_values]),
           delimiter=",", header="n,ImaginaryPart", comments="",
           fmt=["%d", "%.12f"])
print(f"[P1] 資料儲存至 {DATA_DIR / 'zeros_full.csv'}")

# 圖表
gaps = np.diff(t_values)
t_mid = (t_values[:-1] + t_values[1:]) / 2
mean_spacing = 2 * np.pi / np.log(t_mid / (2 * np.pi))
normalized_gaps = gaps / mean_spacing

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(f"Riemann Zeta Zeros — First {N_ZEROS} Non-trivial Zeros", fontsize=14)

ax = axes[0, 0]
ax.plot(indices, t_values, "b-", lw=0.5)
ax.set_xlabel("Zero index n"); ax.set_ylabel("Imaginary part t")
ax.set_title("Zero Height vs Index"); ax.grid(alpha=0.3)

ax = axes[0, 1]
ax.plot(indices[:-1], gaps, "g.", ms=1, alpha=0.5)
ax.set_xlabel("Zero index n"); ax.set_ylabel("Gap")
ax.set_title("Successive Zero Spacings"); ax.grid(alpha=0.3)

ax = axes[1, 0]
ax.hist(normalized_gaps, bins=60, density=True, alpha=0.7, color="steelblue", label="Data")
s = np.linspace(0, 4, 200)
gue_pdf = (np.pi * s / 2) * np.exp(-np.pi * s**2 / 4)
ax.plot(s, gue_pdf, "r-", lw=2, label="GUE")
ax.set_xlabel("Normalized spacing s"); ax.set_ylabel("Density")
ax.set_title("Spacing Distribution vs GUE"); ax.legend(); ax.grid(alpha=0.3)

ax = axes[1, 1]
ax.hist(t_values, bins=60, density=True, alpha=0.7, color="darkorange")
ax.set_xlabel("t"); ax.set_ylabel("Density")
ax.set_title("Distribution of Zero Heights"); ax.grid(alpha=0.3)

plt.tight_layout()
fig.savefig(FIG_DIR / "p1_zero_distribution.png", dpi=150)
print(f"[P1] 圖表儲存至 {FIG_DIR / 'p1_zero_distribution.png'}")
plt.close()

# KS 檢定
def gue_cdf(x):
    return 1 - np.exp(-np.pi * x**2 / 4)
ks_stat, ks_p = ks_1samp(normalized_gaps, gue_cdf)
print(f"[P1] KS vs GUE: stat={ks_stat:.6f}  p-value={ks_p:.6e}")

meta = {
    "n_zeros": N_ZEROS, "dps": MP_DPS,
    "elapsed_s": round(elapsed, 1),
    "last_t": float(t_values[-1]),
    "mean_gap": float(np.mean(gaps)),
    "ks_GUE_stat": round(ks_stat, 6), "ks_GUE_p": float(ks_p),
}
with open(DATA_DIR / "metadata.json", "w") as f:
    json.dump(meta, f, indent=2)

print(f"[P1] P1 完成! 目錄: {DATA_DIR}")
