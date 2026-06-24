"""
RTL - P2: Poisson 隨機點集對比分析
目標：判斷黎曼零點的 H1 拓撲特徵是否統計顯著
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from ripser import ripser
import time

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FIG_DIR  = Path(__file__).resolve().parents[1] / "figures" / "p2"
FIG_DIR.mkdir(parents=True, exist_ok=True)

N_POINTS = 300
N_TRIALS = 10       # Poisson 重複次數 (減少以加速)

print(f"[P2-poisson] 載入零點資料 ...")
t_full = np.loadtxt(DATA_DIR / "zeros_odlyzko_100k.txt")
t_vals = t_full[:N_POINTS]

def zero_embedding_gap_vs_index(t):
    gaps = np.diff(t)
    mean_g = np.mean(gaps)
    X = np.column_stack([np.arange(len(gaps)) / len(gaps), gaps / mean_g])
    return X

def zero_embedding_mod1(t):
    t_mod = t % 1
    X = np.column_stack([t_mod[:-1], t_mod[1:]])
    return X

def poisson_gap_embedding(n):
    pts = np.sort(np.random.uniform(0, 1, n))
    gaps = np.diff(pts)
    mean_g = np.mean(gaps)
    X = np.column_stack([np.arange(len(gaps)) / len(gaps), gaps / mean_g])
    return X

def poisson_mod1_embedding(n):
    X = np.random.uniform(0, 1, (n - 1, 2))
    return X

def count_h1_bars(X, label=""):
    result = ripser(X, maxdim=1, distance_matrix=False)
    dgm = result['dgms'][1]
    if len(dgm) == 0:
        return 0, 0, 0, 0
    births = dgm[:, 0]
    deaths = dgm[:, 1]
    finite = np.isfinite(deaths)
    lifetimes = deaths[finite] - births[finite]
    max_life = np.max(lifetimes) if len(lifetimes) > 0 else 0
    persistent = int(np.sum(lifetimes > 0.1 * max_life)) if max_life > 0 else 0
    return len(dgm), persistent, np.mean(lifetimes) if len(lifetimes) > 0 else 0, max_life

# ── 1. Gap vs Index embedding ──
print(f"\n[P2-poisson] === Gap vs Index ===")
X_zero = zero_embedding_gap_vs_index(t_vals)
h1_zero, pers_zero, mean_life_zero, max_life_zero = count_h1_bars(X_zero, "zero")
print(f"  Zeros: H1={h1_zero}, persistent={pers_zero}, mean_life={mean_life_zero:.4f}")

poisson_h1 = []
poisson_pers = []
poisson_mean_life = []
poisson_max_life = []
print(f"  Poisson trials ({N_TRIALS} runs)...", end="", flush=True)
for i in range(N_TRIALS):
    X_poi = poisson_gap_embedding(N_POINTS)
    h1, pers, ml, mx = count_h1_bars(X_poi, f"poisson-{i}")
    poisson_h1.append(h1)
    poisson_pers.append(pers)
    poisson_mean_life.append(ml)
    poisson_max_life.append(mx)
    print(".", end="", flush=True)
print(" done")

poisson_h1 = np.array(poisson_h1)
poisson_pers = np.array(poisson_pers)

print(f"  Poisson: H1 mean={np.mean(poisson_h1):.1f}+-{np.std(poisson_h1):.1f}, "
      f"persistent mean={np.mean(poisson_pers):.1f}+-{np.std(poisson_pers):.1f}")
print(f"  Zeros  : H1={h1_zero}, persistent={pers_zero}")
print(f"  Z-test : H1 z={(h1_zero - np.mean(poisson_h1))/np.std(poisson_h1):.2f} sigma")

# ── 2. Mod 1 embedding ──
print(f"\n[P2-poisson] === Mod 1 ===")
X_zero_mod = zero_embedding_mod1(t_vals)
h1_zero_m, pers_zero_m, ml_zero_m, mx_zero_m = count_h1_bars(X_zero_mod, "zero-mod")
print(f"  Zeros: H1={h1_zero_m}, persistent={pers_zero_m}, mean_life={ml_zero_m:.4f}")

poi_h1_m = []
poi_pers_m = []
print(f"  Poisson trials ({N_TRIALS} runs)...", end="", flush=True)
for i in range(N_TRIALS):
    X_poi = poisson_mod1_embedding(N_POINTS)
    h1, pers, _, _ = count_h1_bars(X_poi, f"poisson-mod-{i}")
    poi_h1_m.append(h1)
    poi_pers_m.append(pers)
    print(".", end="", flush=True)
print(" done")

poi_h1_m = np.array(poi_h1_m)
poi_pers_m = np.array(poi_pers_m)

print(f"  Poisson: H1 mean={np.mean(poi_h1_m):.1f}+-{np.std(poi_h1_m):.1f}, "
      f"persistent mean={np.mean(poi_pers_m):.1f}+-{np.std(poi_pers_m):.1f}")
print(f"  Zeros  : H1={h1_zero_m}, persistent={pers_zero_m}")
print(f"  Z-test : H1 z={(h1_zero_m - np.mean(poi_h1_m))/np.std(poi_h1_m):.2f} sigma")

# ── 圖: 分佈比較 ──
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle(f"Poisson Comparison: First {N_POINTS} Zeros ({N_TRIALS} trials)", fontsize=13)

ax = axes[0]
ax.hist(poisson_h1, bins=15, alpha=0.7, color="gray", label=f"Poisson (mean={np.mean(poisson_h1):.1f})")
ax.axvline(h1_zero, color="red", lw=2, label=f"Zeros ({h1_zero})")
ax.set_xlabel("H1 bar count"); ax.set_ylabel("Frequency")
ax.set_title("Gap vs Index"); ax.legend(); ax.grid(alpha=0.3)

ax = axes[1]
ax.hist(poi_h1_m, bins=15, alpha=0.7, color="gray", label=f"Poisson (mean={np.mean(poi_h1_m):.1f})")
ax.axvline(h1_zero_m, color="red", lw=2, label=f"Zeros ({h1_zero_m})")
ax.set_xlabel("H1 bar count"); ax.set_ylabel("Frequency")
ax.set_title("Mod 1"); ax.legend(); ax.grid(alpha=0.3)

plt.tight_layout()
fig.savefig(FIG_DIR / "p2_poisson_comparison.png", dpi=150)
print(f"\n[P2-poisson] 圖表儲存: {FIG_DIR / 'p2_poisson_comparison.png'}")
plt.close()

# ── 結論 ──
print(f"\n[P2-poisson] ═══════════════════════════════════")
print(f"[P2-poisson] 結論")
print(f"[P2-poisson] ═══════════════════════════════════")
if (h1_zero > np.percentile(poisson_h1, 95) or h1_zero_m > np.percentile(poi_h1_m, 95)):
    print(f"  >>> 黎曼零點的拓撲特徵在統計上顯著 (超出 Poisson 95% CI)")
else:
    print(f"  >>> 黎曼零點的拓撲特徵與 Poisson 隨機點集無顯著差異")
