"""
RTL - P2: 持久同調分析 (Persistent Homology)
目標：探測黎曼零點分佈在高維度下的拓撲特徵結構
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from ripser import ripser
from persim import plot_diagrams
import time

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FIG_DIR  = Path(__file__).resolve().parents[1] / "figures" / "p2"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# ── 配置 ──
N_POINTS = 500            # 點雲大小 (先測試 500，後續可擴大)
EMBEDDING_DIM = 2        # 嵌入維度 (2D → 可視化 + H1 loop 偵測)
# ─────────────────

# 載入 100k 零點資料 (從 2M 載入前段更快)
print(f"[P2] 載入零點資料 ...")
t_full = np.loadtxt(DATA_DIR / "zeros_odlyzko_100k.txt")
t_vals = t_full[:N_POINTS]
n = len(t_vals)
print(f"[P2] 使用前 {n} 個零點進行 TDA")

def build_point_cloud_embedding(t, method="consecutive"):
    """
    將 1D 零點序列嵌入到 2D 點雲

    method:
      "consecutive": (t_i, t_{i+1}) → 相鄰零點對
      "gap_vs_index": (i/N, gap_i / mean_gap) → 標準化間距
      "mod1": (t_i mod 1, t_{i+1} mod 1) → 模 1 週期結構
      "normalized": (i/N, cumulative_gap / t) → 累積分佈
    """
    if method == "consecutive":
        X = np.column_stack([t[:-1], t[1:]])
        label = f"(t_n, t_{{n+1}}) — Consecutive Pairs"
    elif method == "gap_vs_index":
        gaps = np.diff(t)
        mean_g = np.mean(gaps)
        X = np.column_stack([np.arange(len(gaps)) / len(gaps), gaps / mean_g])
        label = f"(index/N, gap/mean_gap) — Normalized Gaps"
    elif method == "mod1":
        t_mod = t % 1
        X = np.column_stack([t_mod[:-1], t_mod[1:]])
        label = f"(t_n mod 1, t_{{n+1}} mod 1) — Modular Structure"
    elif method == "normalized":
        gaps = np.diff(t)
        cum_gap = np.cumsum(gaps)
        X = np.column_stack([np.arange(len(gaps)) / len(gaps), cum_gap / t[1:]])
        label = f"(i/N, cumulative_gap/t) — Normalized Path"
    else:
        raise ValueError(f"Unknown method: {method}")
    return X, label

def compute_persistence(X, title):
    """計算 Vietoris-Rips 持久同調"""
    print(f"[P2] 計算 {title} ...")
    t0 = time.time()
    result = ripser(X, maxdim=2, distance_matrix=False)
    elapsed = time.time() - t0
    print(f"  H0: {len(result['dgms'][0])} bars, H1: {len(result['dgms'][1])} bars, "
          f"H2: {len(result['dgms'][2])} bars, 耗時 {elapsed:.1f}s")
    return result

def plot_persistence(result, title, filename):
    """畫出 Persistence Diagram + Barcode"""
    dgms = result['dgms']
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle(f"P2: {title}", fontsize=13)

    # Persistence Diagram
    ax = axes[0]
    plot_diagrams(dgms, ax=ax, show=False)
    ax.set_title("Persistence Diagram")

    # Barcode
    ax = axes[1]
    colors = ['steelblue', 'coral', 'seagreen']
    labels = ['H0', 'H1', 'H2']
    for dim in range(min(3, len(dgms))):
        bars = dgms[dim]
        if len(bars) == 0:
            continue
        births = bars[:, 0]
        deaths = bars[:, 1]
        # 將無限死亡設為最大值的 1.1 倍
        max_finite = np.max(deaths[np.isfinite(deaths)]) if np.any(np.isfinite(deaths)) else 1
        deaths[np.isinf(deaths)] = max_finite * 1.1
        sorted_idx = np.argsort(births)
        for i, idx in enumerate(sorted_idx):
            ax.plot([births[idx], deaths[idx]], [i, i],
                    color=colors[dim], lw=1.5, alpha=0.7)
        ax.text(max_finite * 1.15, len(bars) / 2, labels[dim],
                color=colors[dim], fontweight='bold', va='center')

    ax.set_xlabel("Filtration value ε")
    ax.set_ylabel("Bar index")
    ax.set_title("Persistence Barcode")
    ax.grid(alpha=0.2)

    plt.tight_layout()
    fig.savefig(FIG_DIR / filename, dpi=150)
    print(f"[P2] 圖表已儲存: {FIG_DIR / filename}")
    plt.close()

# ════════════════════════════════════════════════════
# 主程式
# ════════════════════════════════════════════════════

# 策略 1: 相鄰零點對 (t_n, t_{n+1})
X1, label1 = build_point_cloud_embedding(t_vals, "consecutive")
r1 = compute_persistence(X1, label1)
plot_persistence(r1, label1, "p2_consecutive_pairs.png")

# 策略 2: 標準化間距
X2, label2 = build_point_cloud_embedding(t_vals, "gap_vs_index")
r2 = compute_persistence(X2, label2)
plot_persistence(r2, label2, "p2_gap_vs_index.png")

# 策略 3: 模 1 結構
X3, label3 = build_point_cloud_embedding(t_vals, "mod1")
r3 = compute_persistence(X3, label3)
plot_persistence(r3, label3, "p2_mod1_structure.png")

# 策略 4: 累積分佈路徑
X4, label4 = build_point_cloud_embedding(t_vals, "normalized")
r4 = compute_persistence(X4, label4)
plot_persistence(r4, label4, "p2_normalized_path.png")

# ── 摘要 ──
print(f"\n[P2] ═══════════════════════════════════════")
print(f"[P2] 拓撲特徵摘要 (前 {n} 個零點)")
print(f"[P2] ═══════════════════════════════════════")
embeddings = [
    ("consecutive", label1, r1),
    ("gap_vs_index", label2, r2),
    ("mod1", label3, r3),
    ("normalized", label4, r4),
]
for key, label, result in embeddings:
    n_h1 = len(result['dgms'][1])
    persistent_h1 = 0
    if n_h1 > 0:
        deaths = result['dgms'][1][:, 1]
        births = result['dgms'][1][:, 0]
        lifetimes = deaths - births
        persistent_h1 = int(np.sum(lifetimes > 0.1 * np.max(deaths[np.isfinite(deaths)])))
    print(f"  {label}:")
    print(f"    H0 bars = {len(result['dgms'][0])}")
    print(f"    H1 bars = {n_h1} (persistent > 10%% max: {persistent_h1})")
    print(f"    H2 bars = {len(result['dgms'][2])}")

# ── 後續: 比較 Poisson ──
print(f"\n[P2] 下一步: 生成 Poisson 隨機點集對照組以判斷顯著性")
