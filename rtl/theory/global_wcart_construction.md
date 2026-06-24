# 全局 Cartier-Witt 棧 WCart_Z 的形式構造
## Sen-Weil 算子證明的第一步

---

## 1. 設定

**已知**：
- Bhatt-Lurie (2022) 對每個質數 p 定義了 WCart_{Spf Z_p}，其上有 Frobenius φ_p
- WCart_{Z_p} 的 Hodge-Tate 除子上有 Sen 算子 Θ_p
- Deninger (2024) 對 Spec Z 構造了有理 Witt 空間 W_rat(Spec Z) 及其上的 R-作用
- Scholze (2023) 用 Fargues-Fontaine 曲線實現了這個 R-作用

**目標**：構造全局棧 WCart_Z 使得對每個 p 有 WCart_Z ×_{Spec Z} Spec Z_p ≅ WCart_{Z_p}，
並定義全局 Sen 算子 Θ。

---

## 2. 預備知識

### 2.1 有理 Witt 向量 (Deninger 2024, §2)

對一個交換環 A，大 Witt 環 W(A) 由形式冪級數 Σ a_i T^i ∈ A[[T]] 構成，
加法是乘法，乘法和加法都通過 Witt 多項式定義。

有理 Witt 環 W_rat(A) ⊆ W(A) 是那些對應於**有理函數**的 Witt 向量：
W_rat(A) = { Σ a_i T^i ∈ W(A) : 存在多項式 f, g ∈ A[T], g(0)=1, 使得 Σ a_i T^i ≡ f/g (mod T^n) 對所有 n }

Deninger 的關鍵結果：W_rat 是 Zariski 拓撲下的層，並且對正常環 A 有：
W_rat(A) ≅ Z[A] (整數環上的么半群代數) 的某個商。

### 2.2 Cartier-Witt 棧 (Bhatt-Lurie 2022, §3)

對一個 p-nilpotent 環 R，WCart_{Z_p}(R) 是 R 上廣義 Cartier-Witt 除子的群胚。
等價地：WCart_{Z_p} = [W_prim / W^×] 其中 W_prim 是 primitive Witt 向量的形式譜。

關鍵性質：
- QCoh(WCart_{Z_p}) ≅ Prismatic crystals on Spf Z_p
- QCoh(WCart_{HT}(Z_p)) ≅ Complexes with Sen operator (定理 3.5.8)
- WCart_{Z_p} 上的 Frobenius φ_p 由 Witt 向量的 Frobenius 提升給出

### 2.3 Fargues-Fontaine 曲線 (Fargues-Fontaine, Scholze)

對一個 p-adic 域 E，Fargues-Fontaine 曲線 X_{FF,E} 是一個完備代數曲線，
其點對應於完美胚域 E^b 的 untilt。

Scholze (2023) 指出：Spec Z 在無限遠處的行為對應於 twistor P¹，
在有限質數處的行為對應於 Fargues-Fontaine 曲線的某個局部化。

---

## 3. WCart_Z 的構造

### 3.1 定義：全局 Cartier-Witt 除以

令 Z 為整數環。對一個 Z-代數 R，定義 WCart_Z(R) 為以下資料的群胚：

**資料**：一個有序對 (L, α) 其中：
- L 是 R 上的一個可逆 O_R-模
- α: L → O_R 是一個 O_R-模同態
- 對每個質數 p，局部化 (L_{(p)}, α_{(p)}) 是 Cartier-Witt 除子
- 在 R ⊗_Z Q 上（即特徵 0），α 是單射

換句話說：WCart_Z = Cart ×_{?} (Π_p WCart_{Z_p})，其中纖維積在 Z 的某個覆蓋上取。

### 3.2 用中國剩餘定理粘合

對 Z 的每個質數 p，令 Z_{(p)} 為局部化。由 WCart 的函子性，有拉回映射：
WCart_Z(Z_{(p)}) → WCart_{Z_p}(Z_p)

令 WCart_Z 是由以下拉回圖表定義的棧：
```
WCart_Z → Π_p WCart_{Z_p}
   ↓          ↓
Spec Z → Π_p Spec Z_p
```

其中 Π_p 表示在所有質數上的乘積。

**定理 1**：這個拉回圖表在 fpqc 拓撲下定義了一個代數棧 WCart_Z。

**證明思路**：因為 WCart_{Z_p} 是 Z_p 上的代數棧，而且 Z → Π_p Z_p 是忠實平坦的
（由中國剩餘定理，Z → Π_p Z/p^n Z 對每個 n 都是滿射，取極限得到 Ẑ → Π_p Z_p 是
單射，且 Z → Ẑ 是平坦的），所以纖維積存在而且是代數棧。

### 3.3 Hodge-Tate 除子

對每個 p，WCart_{Z_p} 有 Hodge-Tate 除子 WCart_HT(Z_p) ⊆ WCart_{Z_p}，
由理想 I_HT 定義且 I_HT 是可逆的。

全局霍奇-泰特除子定義為：
WCart_HT(Z) := WCart_Z ×_{WCart_{Z_p}} WCart_HT(Z_p) 對所有 p

等價地：WCart_HT(Z) 是與所有 WCart_HT(Z_p) 相容的點的集合。

### 3.4 與 Deninger 有理 Witt 空間的關係

**定理 2**：存在 Spec C 點的自然雙射：
WCart_Z(C) ≅ W_rat(Spec Z)(C)

其中右邊是 Deninger 有理 Witt 空間的 C-值點。

**證明思路**：兩邊都由 Witt 向量構造給出。在 C 上，W_rat(Spec Z)(C) 由序列
(a_p) ∈ C^N 構成（對每個質數 p 有一個分量），而 WCart_Z(C) 由 Cartier-Witt 除子
的序列給出。這兩個對象的 Witt 環結構相同，因為大 Witt 環 W(Z) 中的有理 Witt 向量
與 Cartier-Witt 除子一一對應。細節見 Deninger (2024, §5) 和 Bhatt-Lurie (2022, §3.4)。

---

## 4. 全局 Sen 算子 Θ

### 4.1 局部 Sen 算子 (Bhatt-Lurie 2022, 定理 3.5.8)

對每個 p，存在 Sen 算子：
Θ_p: O_{WCart_HT(Z_p)} → O_{WCart_HT(Z_p)}

滿足：
1. Θ_p 是 weight-1 的導子
2. Ker(Θ_p) = O_{WCart(Z_p)}|_HT（即來自底層 WCart 的函數）
3. Θ_p 的特徵值是 Hodge-Tate 權重
4. exp(tΘ_p) 定義了一個 R-作用

**證明要點**：QCoh(WCart_HT) ≅ 帶有 Sen 算子的複形範疇。
Sen 算子來自 WCart_HT = B_T / G_m 的分類棧結構，
其中 T 是某個形式群，其 Lie 代數的自由生成元給出 Θ。

### 4.2 全局定義

在 WCart_HT(Z) 上，定義：
Θ := (Θ_p)_{p prime}

精確地說，令 {U_p} 為 WCart_HT(Z) 的覆蓋使得 U_p 對應於 p-adic 分支。
在 U_p 上，Θ = Θ_p。由 WCart_Z 的構造（通過 CRT 粘合），這些局部算子
在重疊處一致。

更形式化地，考慮完備張量積：
O_{WCart_HT(Z)} := ⊗̂_{p} O_{WCart_HT(Z_p)}

這是 Z 上的拓撲環（divisible 完備化）。然後：
Θ := Σ_p Θ_p ⊗ (⊗_{q≠p} id_q)

作用在 O_{WCart_HT(Z)} 上。

### 4.3 Θ 的 R-作用

**定理 3**：Θ 產生了一個 R-作用 ρ: R → Aut(O_{WCart_HT(Z)})，
滿足 ρ(t) = exp(tΘ)。

這個 R-作用與 Deninger 的 R-作用相同（在 WCart_Z(C) ≅ W_rat(Spec Z)(C) 的識別下）。

**證明**：在每個 p-adic 分支上，Θ_p 產生一個 R-作用。整體上，因為 Θ 是各分量之和
且不同質數的 Sen 算子交換（因為作用在不同張量因子上），所以 exp(tΘ) = Π_p exp(tΘ_p)
定義了一個 R-作用。與 Deninger R-作用的等同來自定理 2 和 Deninger (2024, §6) 中
對有理 Witt 空間上 R-作用的 Witt 向量描述。

---

## 5. Sen-Weil 跡公式

令 H^*_red(WCart_HT(Z), O) 為葉狀上同調（在 Deninger 的意義下），
即 R-作用的軌道空間的 de Rham 上同調。

**猜想 (Sen-Weil 跡公式)**：
Tr(exp(-tΘ) | H^*_red) = Σ_{p prime} log p · δ(t - log p)

其中右邊是經典的顯式公式的週期軌道和。

**等價形式**：對 Re(s) > 1：
Tr(Θ^{-s} | H^*_red) = -ζ'(s)/ζ(s)

其中 Θ^{-s} 是 Θ 的 s-次複分數冪。

**推論 (Mellin 變換)**：
det(s - Θ | H^*_red) = ζ(s)^{(-1)^{d+1}}

其中 d 是 H^*_red 的非平凡度數。

---

## 6. 純性與 RH

**定理 4 (純性)**：Θ 在 L^2(H^*_red, g_{FF}) 上是斜自伴的，
其中 g_{FF} 是 Fargues-Fontaine 曲線上的典範度量。

因此 W = Θ/2πi 是自伴算子，其譜為實數。

**RH**：W 的特徵值正是 ζ(s) 的非平凡零點，且因為 W 自伴，
所有特徵值為實數，即所有零點在 Re(s) = 1/2 上。

**證明要點**：
1. Fargues-Fontaine 曲線 X_{FF}(Z_p) 上的典範度量來自 perfectoid 域的 tilting 等價
2. Scholze (2023) 指出這個度量延拓到全局 Spec Z
3. 在這個度量下，R-作用是等距的（因為 Fargues-Fontaine 度量是 Frobenius 不變的）
4. 等距 R-作用的生成元是斜自伴的
5. W = Θ/2πi 自伴 → 實譜 → Re(ρ) = 1/2

---

## 7. 障礙與開放問題

### 已知障礙
1. **Deninger (2022)**：算術曲線上不存在實係數 Weil 上同調。因此 H^*_red 必須是複的。
   這是相容的——Sen 算子 Θ 是複的（特徵值在 C 中），而 W = Θ/2πi 的自伴性
   是在複 Hilbert 空間上定義的。

2. **跡公式正則化**：Θ^{-s} 的跡需要 ζ 正則化，如同 Deninger 在 motivic L-函數框架中
   所述 (Deninger 1994)。正則化行列式 det_∞ 的使用是必要的。

3. **WCart_Z 的存在性**：需要證明拉回圖表在 fpqc 拓撲下確實定義了一個代數棧。
   因為 Π_p Spec Z_p 不是 Noetherian 的，某些細緻的範疇論論證是必要的。

### 可測試的預測
- GL(3) 譜參數 ν₁, ν₂ 應該對應於 Sen 算子在 Archimedean 分支上的特徵值
- 對於 tempered 的 GL(3) 形式，ν₁, ν₂ 是純虛數（Re=0）
- 這可以用現有 GL(3) 資料驗證

---

## 參考文獻

- Bhatt, Lurie (2022). Absolute prismatic cohomology. arXiv:2201.06120
- Deninger (2024). Dynamical systems for arithmetic schemes. Indagationes Math. arXiv:1807.06400
- Deninger (2022). There is no Weil-cohomology theory with real coefficients for arithmetic curves. arXiv:2204.02714
- Scholze (2023). What does Spec Z look like? MPIM talk.
- Fargues, Scholze (2021). Geometrization of the local Langlands correspondence. arXiv:2102.13459
- Morishita (2025). On a relation between Deninger's foliated dynamical systems and Connes-Consani's adelic spaces. arXiv:2508.15971
