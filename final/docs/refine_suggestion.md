# Refine Suggestions for NTHU NLP Final Report

> 針對 `overleaf_latex/nthu_nlp_final_2025.tex` 的修改建議

---

## 待處理建議

### 3. Section 1.3 - Ranking Sensitivity to Distribution Shift
- **重要性**：⭐⭐⭐⭐ 高 (影響技術嚴謹性)
- **難度**：🔧 中等
- **問題**：「ranking sensitive to distribution shift」的原因說明不夠清楚
- **建議**：補充解釋為什麼 ranking 會特別對 distribution shift 敏感 (相較於 absolute error)
- **狀態**：❌ 待處理

### 1. Section 1.2 - SRCC vs MSE 的挑戰性
- **重要性**：⭐⭐⭐ 中
- **難度**：🔨 簡單
- **問題**：目前沒有說明為什麼 SRCC 對 MSE 是 challenging 的
- **建議**：補充說明 SRCC 相較於 MSE 為何更具挑戰性的原因 (e.g. MSE 最小化不保證排序正確)
- **狀態**：❌ 待處理

### 5. Figure 1 - 缺少符號與維度說明
- **重要性**：⭐⭐⭐ 中
- **難度**：🔨 簡單
- **問題**：
  - 圖旁邊的 `w` 在文章中沒有解釋代表什麼
  - `4x1024x1024` 需要說明這是什麼東西的 dimension
- **建議**：在圖說明或正文中補充 `w` 的定義以及維度的含義
- **狀態**：❌ 待處理

---

## 已完成建議

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
