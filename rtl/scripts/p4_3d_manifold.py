"""
RTL - P4: 3D Manifold Projection & Visualization
Project high-dimensional zero structure into 3D space.
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.decomposition import PCA

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FIG_DIR  = Path(__file__).resolve().parents[1] / "figures" / "p4"
FIG_DIR.mkdir(parents=True, exist_ok=True)

print("[P4] Loading zeros ...")
t = np.loadtxt(DATA_DIR / "zeros_odlyzko_100k.txt")
N = len(t)
print(f"[P4] Using first {N:,} zeros")

gaps = np.diff(t)
sg = gaps / np.mean(gaps)  # normalized gaps

# ============================================================
#  1. 3D Delay Embedding: (t_n, t_{n+1}, t_{n+2})
# ============================================================
print("[P4] 3D delay embedding ...")
n_pts = 3000
t3 = np.column_stack([t[:n_pts], t[1:n_pts+1], t[2:n_pts+2]])

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(t3[:, 0], t3[:, 1], t3[:, 2], c=np.arange(n_pts),
           cmap='viridis', s=1, alpha=0.6)
ax.set_xlabel("t_n"); ax.set_ylabel("t_{n+1}"); ax.set_zlabel("t_{n+2}")
ax.set_title("3D Delay Embedding: (t_n, t_{n+1}, t_{n+2})")
fig.savefig(FIG_DIR / "p4_delay_embedding.png", dpi=150)
plt.close()

# ============================================================
#  2. 3D Gap Dynamics: (gap_n, gap_{n+1}, gap_{n+2})
# ============================================================
print("[P4] 3D gap phase space ...")
n_pts = 5000
sg3 = np.column_stack([sg[:n_pts], sg[1:n_pts+1], sg[2:n_pts+2]])

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(sg3[:, 0], sg3[:, 1], sg3[:, 2], c=np.arange(n_pts),
           cmap='plasma', s=1, alpha=0.5)
ax.set_xlabel("gap_n"); ax.set_ylabel("gap_{n+1}"); ax.set_zlabel("gap_{n+2}")
ax.set_title("3D Gap Phase Space: (gap_n, gap_{n+1}, gap_{n+2})")
fig.savefig(FIG_DIR / "p4_gap_phase.png", dpi=150)
plt.close()

# ============================================================
#  3. PCA on Sliding Window Feature Vectors
# ============================================================
print("[P4] PCA on sliding windows ...")
window = 100
stride = 10
n_windows = (N - window) // stride
features = np.zeros((n_windows, window))
for i in range(n_windows):
    start = i * stride
    seg = sg[start:start + window]
    features[i] = seg[:window]

pca = PCA(n_components=3)
proj = pca.fit_transform(features)
print(f"  PCA explained variance: {pca.explained_variance_ratio_}")
print(f"  Cumulative: {np.sum(pca.explained_variance_ratio_):.3f}")

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(proj[:, 0], proj[:, 1], proj[:, 2],
                c=np.arange(n_windows), cmap='twilight', s=2, alpha=0.6)
ax.set_xlabel("PC1"); ax.set_ylabel("PC2"); ax.set_zlabel("PC3")
ax.set_title(f"PCA of Windowed Gaps (window={window})")
cbar = fig.colorbar(sc, ax=ax, shrink=0.5)
cbar.set_label("Window index")
fig.savefig(FIG_DIR / "p4_pca_gaps.png", dpi=150)
plt.close()

# ============================================================
#  4. Plotly Interactive 3D (saved as HTML)
# ============================================================
print("[P4] Plotly interactive 3D ...")
try:
    import plotly.graph_objects as go
    import plotly.io as pio

    sg3_sample = sg3[::5]  # subsample for performance
    colors = np.arange(len(sg3_sample))

    fig_pl = go.Figure(data=[
        go.Scatter3d(
            x=sg3_sample[:, 0], y=sg3_sample[:, 1], z=sg3_sample[:, 2],
            mode='markers',
            marker=dict(size=1.5, color=colors, colorscale='Plasma',
                        showscale=True, colorbar=dict(title="Index")),
            text=[f"n={i}<br>gap={g[0]:.3f}" for i, g in enumerate(sg3_sample)],
            hoverinfo='text'
        )
    ])
    fig_pl.update_layout(
        title="3D Gap Phase Space (Interactive)",
        scene=dict(xaxis_title="gap_n", yaxis_title="gap_{n+1}",
                   zaxis_title="gap_{n+2}"),
        width=900, height=700
    )
    pio.write_html(fig_pl, str(FIG_DIR / "p4_gap_phase_interactive.html"))
    print(f"  Saved: {FIG_DIR / 'p4_gap_phase_interactive.html'}")
except Exception as e:
    print(f"  Plotly skipped: {e}")

# ============================================================
#  5. Rotating Animation (multi-angle frames → GIF)
# ============================================================
print("[P4] Rotating animation frames ...")
fig = plt.figure(figsize=(8, 7))
ax = fig.add_subplot(111, projection='3d')
n_ani = 5000
sg3_ani = np.column_stack([sg[:n_ani], sg[1:n_ani+1], sg[2:n_ani+2]])

angles = np.linspace(0, 360, 37)[:-1]  # 36 frames (10 deg each)
anim_dir = FIG_DIR / "animation_frames"
anim_dir.mkdir(parents=True, exist_ok=True)

for idx, angle in enumerate(angles):
    ax.clear()
    ax.scatter(sg3_ani[:, 0], sg3_ani[:, 1], sg3_ani[:, 2],
               c=np.arange(n_ani), cmap='plasma', s=0.5, alpha=0.4)
    ax.view_init(elev=20, azim=angle)
    ax.set_xlabel("gap_n"); ax.set_ylabel("gap_{n+1}"); ax.set_zlabel("gap_{n+2}")
    ax.set_title(f"3D Gap Phase Space (angle={angle:.0f})")
    fig.savefig(anim_dir / f"frame_{idx:03d}.png", dpi=120)
    if (idx + 1) % 10 == 0:
        print(f"  Frame {idx+1}/{len(angles)}")
plt.close()

try:
    from PIL import Image
    frames = []
    for idx in range(len(angles)):
        f = anim_dir / f"frame_{idx:03d}.png"
        if f.exists():
            frames.append(Image.open(f))
    if frames:
        gif_path = FIG_DIR / "p4_gap_phase_rotation.gif"
        frames[0].save(gif_path, save_all=True, append_images=frames[1:],
                       duration=150, loop=0, optimize=True)
        print(f"  GIF saved: {gif_path}")
except Exception as e:
    print(f"  GIF creation skipped (need Pillow): {e}")

# ============================================================
#  6. Prime-Zero Joint 3D Visualization
# ============================================================
print("[P4] Prime-zero 3D joint visualization ...")
from sympy import primerange

# Use first 100k primes matched against first 100k zeros
n_primes = 2000
primes = list(primerange(2, 20000))[:n_primes]
zeros_sub = t[1:n_primes+1]

# 3D: (prime index, log(prime), zero height) → look for structure
p_idx = np.arange(len(primes))
log_p = np.log(primes)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
sc = ax.scatter(p_idx, log_p, zeros_sub[:len(primes)],
                c=zeros_sub[:len(primes)], cmap='coolwarm', s=3, alpha=0.7)
ax.set_xlabel("Prime index"); ax.set_ylabel("log(prime)"); ax.set_zlabel("Zero height t")
ax.set_title("Prime-Zero Joint Distribution")
cbar = fig.colorbar(sc, ax=ax, shrink=0.5)
cbar.set_label("Zero height")
fig.savefig(FIG_DIR / "p4_prime_zero_3d.png", dpi=150)
plt.close()

# ============================================================
#  Summary
# ============================================================
print(f"\n[P4] All outputs saved to: {FIG_DIR}")
print(f"  Files:")
for f in sorted(FIG_DIR.iterdir()):
    size = f.stat().st_size
    if size > 1000:
        print(f"    {f.name}  ({size//1000} KB)")
    else:
        print(f"    {f.name}  ({size} B)")
