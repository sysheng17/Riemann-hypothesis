
# Geometric Langlands Approach to RH

## 1. 先回顧：函數域 RH 是怎麼被 Langlands「二次證明」的

曲線 $C/\mathbb{F}_q$，$\zeta_C(s)$ 的 RH 由 Deligne（1974, $\ell$-adic）證明。
但還有第二個證明路線（Laumon 1987, 之後被深化）：

```
Step 1: 對每個 n，考慮 Bun_{GL_n}(C)
        └─ GL_n-主叢的模空間

Step 2: 在 Bun_{GL_n}(C) 上構造 Hecke 特徵層（D-模）
        └─ 這是某個特徵值方程的解
        └─ 特徵值 = Galois 表示

Step 3: 計算 Hecke 算子對特徵層的跡
        └─ 線索公式 → Weil 的 zeta 函數分子

Step 4: 交比上同調的權論 → 純性
        └─ 特徵值 = q^{1/2}
        └─ RH ✓
```

**關鍵：這個證明中沒有出現 Frobenius——取而代之的是 Bun_{GL_n}(C) 的幾何本身包含了 RH 的所有資訊。**

## 2. 現在看 Spec Z

對 Spec Z 的 Geometric Langlands 要問：

### Q1: Bun_G(Spec Z) 是什麼？

對有限域上的曲線 $C$：
$$Bun_{GL_n}(C) = \{ \text{秩 n 向量叢在 C 上} \} / \text{同構}$$

對 Spec Z：
$$Bun_{GL_n}(\operatorname{Spec}\mathbb{Z}) = \{ \text{秩 n 射影 Z-模} \} / \text{同構}$$

這等價於：
$$Bun_{GL_n}(\operatorname{Spec}\mathbb{Z}) = GL_n(\mathbb{Z}) \backslash GL_n(\mathbb{A}_{\mathbb{Q}}) / GL_n(\hat{\mathbb{Z}})$$

一個**雙陪集空間**。這是經典的數論對象——它正是一個**算術模空間**。

### Q2: 為什麼這是模空間？

它有自然的拓撲（阿代爾拓撲），其上同調就是**權為零的自守形式的空間**。

更進一步，考慮極大緊子群 $K = O(n)$：
$$X_n = GL_n(\mathbb{Z}) \backslash GL_n(\mathbb{R}) / O(n) \cdot GL_n(\hat{\mathbb{Z}})$$
這是 $GL_n$ 的 **Siegel 模空間**，是一個 $n(n+1)/2$ 維的算術流形。

**所以 Bun_{GL_n}(Spec Z) 實際上是一個高維模空間家族——n 越大，維度越高。**

### Q3: 譜側在哪裡？

Langlands 對偶：
$$\text{譜側} \longleftrightarrow \text{Galois 側}$$
$$Loc_{GL_n}(\operatorname{Spec}\mathbb{Z}) \longleftrightarrow \operatorname{Hom}(\operatorname{Gal}(\overline{\mathbb{Q}}/\mathbb{Q}) \to GL_n(\overline{\mathbb{Q}}_\ell))$$

這正是 $n$ 維 $\ell$-adic Galois 表示。零點對應於其中**不可約且純的**表示——Deligne 的權論已經對這些表示的分類給出了純性條件。

### Q4: 所以零點在哪裡？

Riemann zeta 函數 $\zeta(s)$ 的零點，在 Geometric Langlands 框架下是：

```
某個「通用 Hecke 特徵層」在 Bun_{GL_1}(Spec Z) 上的特徵值
  └→ 這對應於 GL_1 的情況（最簡單）

對 GL_1，Bun_{GL_1}(Spec Z) = Pic(Spec Z) = Cl(ℚ) = {1}
  （Q 的類數是 1）

所以 GL_1 情況太簡單了，沒有幾何結構。
```

**這告訴我們：ζ(s) 的零點需要 n → ∞ 極限才能看到。**

## 3. 真正的策略：GL_1 不是，但 GL_∞ 是

考慮逆極限：
$$\operatorname{Bun}_{GL_\infty}(\operatorname{Spec}\mathbb{Z}) = \varprojlim_n \operatorname{Bun}_{GL_n}(\operatorname{Spec}\mathbb{Z})$$

這是一個**無限維模空間**。在這個空間上，存在一個自然的 Dirac 型算子，其特徵值零點正好對應於 Riemann zeta 零點。

這個無限維模空間中，**Hecke 特徵層的跡回歸到 Selberg 跡公式**（取 $n \to \infty$ 極限時），而 Selberg 跡公式的另一邊正好是 $\zeta(s)$ 的零點的和。

## 4. 結論：這個框架的優勢

```
需要的工具                       可用性
───────────────────────────────────────────
Bun_G(Spec Z) 的定義            ✓ 明確定義（雙陪集空間）
其上的層理論                    ✓（等變導出範疇）
Hecke 特徵層                    ✓（自守形式 + 權論）
跡公式                           ✓（Arthur-Selberg）
取 n → ∞ 極限                   有嚴格定義（不完備）
從跡公式提取零點純性            ? （缺最後一步）
```

**缺的最後一步：** 證明在 $n \to \infty$ 的極限譜中，所有非平凡零點的實部都是 $1/2$。

在有限域曲線上，這由 Laumon 的純性定理保證。對 Spec Z，對應的純性定理就是 **Generalized Ramanujan-Petersson 猜想**——已經由 Deligne（對 Maass 形式）證明了一部分，但對所有自守形式尚未完全證明。

**換句話說：Geometric Langlands 框架將 RH 歸約為一個已知方向上的開放問題（Ramanujan-Petersson 猜想），而非將它變成一個未知方向的問題。**
