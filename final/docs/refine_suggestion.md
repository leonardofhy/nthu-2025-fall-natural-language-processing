# Refine Suggestions for NTHU NLP Final Report

> 針對 `overleaf_latex/nthu_nlp_final_2025.tex` 的修改建議

---

---

## 已完成建議

### ~~7. Section 3.2 - Attention Pooling 公式~~ ✅
- **重要性**：⭐⭐⭐ 中
- **難度**：🔧 中等
- **問題**：缺乏 Attention Pooling 的具體數學定義
- **解決方案**：加入 $\alpha_i = \text{softmax}(\mathbf{w}^\top \tanh(\mathbf{W}\mathbf{h}_i))$ 公式
- **狀態**：✅ 已完成

### ~~8. Section 3.4 - Ranking Loss 定義~~ ✅
- **重要性**：⭐⭐⭐ 中
- **難度**：🔧 中等
- **問題**：$\mathcal{L}_{\text{ranking}}$ 沒有定義
- **解決方案**：加入 Pairwise Margin Ranking Loss 公式
- **狀態**：✅ 已完成

### ~~10. Figure 1 & 2 輸入格式一致化~~ ✅
- **重要性**：⭐ 低 (視覺性問題)
- **難度**：🔨 簡單
- **解決方案**：將 Fig 2 的縮寫 (`Q`, `A`) 統一改為與 Fig 1 一致的完整單詞 (`Question`, `Answer`)。
- **狀態**：✅ 已完成

### ~~5. Figure 1 - 缺少符號與維度說明~~ ✅
- **重要性**：⭐⭐⭐ 中
- **難度**：🔨 簡單
- **問題**：圖旁的 dimension 標註不夠直觀
- **解決方案**：將數學符號改為更直觀的英文描述 (e.g. `layers × seq × hidden`, `learnable weights`)
- **狀態**：✅ 已完成

### ~~1. Section 1.2 - SRCC vs MSE~~ ✅
- **重要性**：⭐⭐⭐ 中
- **難度**：🔨 簡單
- **問題**：目前沒有說明為什麼 SRCC 對 MSE 是 challenging 的
- **解決方案**：說明 MSE/BCE 是 point-wise loss，不會保留排序關係
- **狀態**：✅ 已完成

### ~~3. Section 1.3 - Ranking Sensitivity~~ ✅
- **重要性**：⭐⭐⭐⭐ 高 (影響技術嚴謹性)
- **難度**：🔧 中等
- **問題**：「ranking sensitive to distribution shift」的原因說明不夠清楚
- **解決方案**：補充說明 ranking 依賴全局排序而非單點誤差，因此對 distribution shift 特別敏感
- **狀態**：✅ 已完成

### ~~4. Table 1 - 術語未提前定義~~ ✅
- **重要性**：⭐⭐⭐⭐⭐ 很高 (影響讀者理解)
- **難度**：🔧 中等
- **問題**：Summary 中有些名詞在 Table 1 出現時還沒被介紹過
- **解決方案**：在 Table 1 caption 加入 forward reference：「WLP (Weighted Layer Pooling) and Soft Spearman Loss are detailed in Sections 3.2 and 3.4, respectively.」
- **狀態**：✅ 已完成

### ~~6. Figure 2 - Epoch 數量標註~~ ✅
- **重要性**：⭐⭐ 低
- **難度**：🔨 簡單
- **問題**：`3+3` 和 `5+5` 的標示不夠明確
- **解決方案**：移除圖內的 `Epochs: 5` 標註，讓 caption 處理細節說明
- **狀態**：✅ 已完成

### ~~2. Metric 引用來源~~ ✅
- **重要性**：⭐⭐ 低
- **難度**：🔨 簡單
- **問題**：缺少比賽 metric 相關的 paper citation
- **解決方案**：在 Section 1.2 加入 Spearman (1904) 引用 [10]
- **狀態**：✅ 已完成
