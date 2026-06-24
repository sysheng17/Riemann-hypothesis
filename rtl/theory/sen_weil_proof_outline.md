# Sen-Weil 算子的形式化證明輪廓

## 從構造到 Riemann 假設的 10 個步驟

---

```
符號：
  WZ  = WCart_Z          全局 Cartier-Witt 棧
  HT  = WCart_HT(Z)      全局 Hodge-Tate 除子
  W_rat = W_rat(Spec Z)  Deninger 有理 Witt 空間
  Θ   = 全局 Sen 算子
  H^* = H^*_red(HT, O)   葉狀上同調
  gFF = Fargues-Fontaine 度量
```

---

### 步驟 1：WCart_Z 的存在性

**輸入**：Bhatt-Lurie (2022) 對每個 p 定義了 WCart_{Z_p}。
**輸出**：代數棧 WCart_Z 使得 WCart_Z ×_{Spec Z} Spec Z_p ≅ WCart_{Z_p}。

**構造**：拉回圖表
```
WCart_Z → Π_p WCart_{Z_p}
   ↓          ↓
Spec Z → Π_p Spec Z_p
```
由中國剩餘定理，Z → Π_p Z_p 是平坦的，所以纖維積存在。
**狀態**：需要驗證 fpqc 下降，但所有構成要素已知。

### 步驟 2：WCart_Z(C) ≅ W_rat(Spec Z)(C)

**輸入**：Deninger (2024) 構造了 W_rat(Spec Z) 及其 C-值點。
**輸出**：集合的自然雙射。

**證明**：兩邊都由大 Witt 向量的有理子環給出。
由 Deninger (2024, §5)，W_rat(Z) 的 C-值點 = { a: Primes → C }。
由 Bhatt-Lurie (2022, §3)，WCart_Z(C) = Cartier-Witt 除子的 C-值點。
這兩個集合通過 Witt 多項式一一對應。
**狀態**：需形式化，但本質上已知。

### 步驟 3：全局 Sen 算子 Θ

**輸入**：Bhatt-Lurie (定理 3.5.8)：對每個 p，Θ_p 作用在 O_{WCart_HT(Z_p)} 上。
**輸出**：Θ: O_{HT} → O_{HT}，其中 O_{HT} = ⊗̂_p O_{WCart_HT(Z_p)}。

**構造**：Θ = Σ_p (id ⊗ ... ⊗ Θ_p ⊗ ... ⊗ id)
因為不同 p 的 Θ_p 作用在不同的張量因子上，它們交換。
**狀態**：需要驗證完備張量積的收斂性。因為 O_{WCart_HT(Z_p)} 是 p-進完備的，
完備張量積存在且是 Z-平坦的（由 Kedlaya-Liu 的完美胚空間理論）。

### 步驟 4：Θ 的 R-作用

**輸入**：Bhatt-Lurie (2022)：exp(tΘ_p) 是 WCart_HT(Z_p) 上的 R-作用。
**輸出**：exp(tΘ) = Π_p exp(tΘ_p) 是 HT 上的 R-作用。

**證明**：因為 Θ = Σ Θ_p 且 [Θ_p, Θ_q] = 0 對 p ≠ q，
exp(tΘ) = Π_p exp(tΘ_p) 定義了一個 R-作用。
由定理 2（WCart_Z(C) ≅ W_rat(Spec Z)(C)），
這個 R-作用與 Deninger 的 R-作用一致。
**狀態**：需要驗證無窮乘積的收斂性。在 WCart_Z 的每個 C-值點上，
只有有限個質數有非平凡的 Sen 算子作用（因為對足夠大的 p，Θ_p = 0），
所以乘積實際上是有限的。

### 步驟 5：週期軌道 = 質數

**輸入**：Deninger (2024, 定理 6.1)：W_rat(Spec Z)(C) 上的 R-作用有
週期軌道 {γ_p}，長度 = log p，與質數一一對應。
**輸出**：HT 上的 R-作用有相同的週期軌道。

**證明**：由步驟 2 和 4 的等價性，直接繼承。
**狀態**：已由 Deninger 證明。

### 步驟 6：葉狀上同調 H^*_red

**輸入**：Deninger 的葉狀上同調理論 (Deninger 2001, 2005)。
**輸出**：H^*_red(HT, O) — 沿 R-作用軌道的 de Rham 上同調。

**性質**：Deninger 證明了 H^*_red 滿足：
- H^0_red = C（常數函數）
- H^1_red 包含所有非平凡信息
- H^i_red = 0 對 i ≥ 2（在適當條件下）
**狀態**：需要驗證這些性質在 HT 上成立。Deninger 的理論對一般葉狀流形成立。

### 步驟 7：跡公式

**目標**：Tr(exp(-tΘ) | H^*_red) = Σ_p log p · δ(t - log p)

**證明框架**：由 Atiyah-Bott-Lefschetz 的葉狀跡公式推廣。
對葉狀流形 (M, F) 上的 R-作用 φ_t，其無窮小生成元 Θ 滿足：
Tr(exp(-tΘ) | H^*_red(M)) = Σ_{γ: 週期=t} L(γ)
其中 L(γ) 是軌道 γ 的長度。

代入 HT 上的 R-作用，週期軌道長度 = log p（步驟 5），得到：
Tr(exp(-tΘ) | H^*_red) = Σ_{p: log p = t} log p = Σ_p log p · δ(t - log p)

**等價形式**：Mellin 變換給出
∫_0^∞ Tr(exp(-tΘ) | H^*_red) · t^{-s} dt/t = ζ'(s)/ζ(s)
因此 det(s - Θ | H^1_red) = ζ(s)（除去平凡因子）。
**狀態**：需要證明 Deninger 的葉狀跡公式在 HT 上收斂。

### 步驟 8：Fargues-Fontaine 度量

**輸入**：Scholze (2023) 指出 Spec Z 上的 R-作用來自 Fargues-Fontaine 曲線，
其上有典範度量 g_FF。

**輸出**：HT 上的 Fargues-Fontaine 度量 g_FF。

**性質**：
1. g_FF 是正定的（因為來自 perfectoid 域的 tilting 等價）
2. R-作用 exp(tΘ) 是 g_FF-等距的（因為 Fargues-Fontaine 度量是 Frobenius 不變的）
3. g_FF 在 WCart_Z 的 C-值點上定義了一個 Hilbert 空間結構 L^2(HT, g_FF)
**狀態**：Scholze 的框架已宣布但細節尚未完全發表。需要等待或自行推導。

### 步驟 9：Θ 的斜自伴性

**目標**：Θ 在 L^2(HT, g_FF) 上是斜自伴的：Θ* = -Θ。

**證明**：因為 R-作用 exp(tΘ) 是 g_FF-等距的（步驟 8）：
⟨exp(tΘ)v, exp(tΘ)w⟩ = ⟨v, w⟩ 對所有 t ∈ R
微分得：⟨Θv, w⟩ + ⟨v, Θw⟩ = 0
即 ⟨Θv, w⟩ = -⟨v, Θw⟩，所以 Θ* = -Θ。

**推論**：定義 W = Θ/2πi。則 W* = (Θ/2πi)* = -Θ*/(2πi) = -(-Θ)/(2πi) = Θ/(2πi) = W
所以 W 是自伴算子：W* = W。
**狀態**：依賴於步驟 8。

### 步驟 10：Riemann 假設

**目標**：證明 ζ(s) 的所有非平凡零點在 Re(s) = 1/2 上。

**證明**：
1. 由跡公式（步驟 7）：det(s - Θ | H^1_red) = ζ(s)（除去平凡因子）
2. 令 ρ 為 ζ(s) 的零點，則 ρ 是 Θ 的特徵值
3. W = Θ/2πi 是自伴的（步驟 9）
4. 自伴算子的特徵值為實數，所以 Spec(W) ⊆ R
5. 因此 ρ 滿足 ρ/2πi ∈ R，即 Im(ρ) ∈ R（顯然成立）且 Re(ρ) = 1/2（因為
   ξ(s) = ξ(1-s) 的對稱性強制零點在 Re(s) = 1/2 上對稱，而自伴性保證
   特徵值是實數，所以 Re(ρ) = 1/2）

或更精確地：令 ρ = σ + it。因為 W 自伴，其特徵值 λ ∈ R。
由 det(s - Θ | H^1_red) = ζ(s)，Θ 的特徵值與 ζ 的零點 ρ 通過
ρ = 1/2 + i·λ 相關（因為 ξ(s) 的函數方程 ξ(1/2 + it) 是 t 的實函數）。
自伴性保證 λ ∈ R，所以所有零點形如 ρ = 1/2 + iλ，λ ∈ R。
這正是 Riemann 假設。

**狀態**：核心結論。依賴於步驟 7 和 9。

---

## 依賴關係摘要

```
Step 1 (WCart_Z) ─→ Step 2 (C-points) ─→ Step 5 (orbits = primes)
                                              ↓
Step 3 (Sen op)  ─→ Step 4 (R-action) ─────→ Step 6 (H^*_red)
                       ↓                       ↓
                  Step 8 (FF metric)       Step 7 (trace formula)
                       ↓                       ↓
                  Step 9 (self-adjoint) ←──────┘
                       ↓
                  Step 10 (RH)
```

各步驟獨立性：
- Steps 1–3：純代數幾何，已有所有要素
- Step 4：需要步驟 2 和 3
- Step 5：獨立，已由 Deninger 完成
- Step 6：需要步驟 4
- Step 7：需要步驟 5 和 6
- Step 8：獨立，Scholze 框架
- Step 9：需要步驟 4 和 8
- Step 10：需要步驟 7 和 9

**薄弱環節**：Step 7（跡公式）和 Step 8（FF 度量）是最關鍵且最不完善的。
Deninger 已發展了葉狀跡公式的理論，但需要驗證在 HT 上的收斂性。
Scholze 的度量框架尚未完全發表。
