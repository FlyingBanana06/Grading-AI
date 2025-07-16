# 2025-07-13

---

## 🧠 二、系統流程設計

### 1. 手寫文字辨識（OCR）

> 技術：使用 AI 模型（如 Google Tesseract, Microsoft OCR, 或專門的深度學習模型如 TrOCR）

* 須考慮筆跡變化與排版不規則
* 對於數學公式可能需要特殊模型（如 MathPix, Im2LaTeX）

### 2. 項目識別與結構分析（可選）

* 將整份考卷切割成題號 + 作答區塊
* 使用圖像分割或視覺分析方法（如 YOLO、Detectron2）

### 3. 自動比對與理解答案

依題型不同會有不同方法：

| 題型  | 技術                           |
| --- | ---------------------------- |
| 選擇題 | OCR + 比對                     |
| 填空題 | NLP 相似度比對（例如詞義匹配、關鍵字比對）      |
| 開放題 | 使用 GPT 之類的大語言模型評分            |
| 數學題 | 使用 Symbolic Matching、或解析步驟邏輯 |

---

## 🗃 三、資料收集與模型訓練（如需自訓）

1. **收集資料**

   * 大量手寫答案與對應標準答案
   * 評分標準（Rubric）

2. **標註與清洗**

   * 人工標註哪些答案對、錯、部分正確
   * 清洗圖片中的雜訊與錯誤辨識

3. **模型訓練（若不用現成）**

   * OCR 模型（若 Tesseract 不夠）
   * NLP 評分模型（如 BERT、GPT Fine-tuning）

---

## 🧪 四、整合與測試

1. **系統整合**

   * 建立 pipeline：圖像輸入 → OCR → NLP → 評分 → 回傳結果
   * 可使用 Python + Flask/Streamlit 建立簡易介面

2. **測試**

   * 使用不同筆跡、題型、解析度做測試
   * 比對人工改卷與 AI 評分的一致性（例如用 Cohen's Kappa 指標）

---

## 🧰 建議用的工具與框架

| 任務    | 工具推薦                              |
| ----- | --------------------------------- |
| OCR   | Tesseract、TrOCR、PaddleOCR         |
| NLP   | spaCy、transformers、OpenAI GPT API |
| 評分    | 自建規則 + ChatGPT API                |
| 圖像處理  | OpenCV、YOLO、Detectron2            |
| 前端/整合 | Streamlit、Gradio、Flask、FastAPI    |

---

pt.2

---

## 🔹 建議系統流程（簡化版）

```
PDF/JPG 檔案 → OCR 辨識 → 語言模型理解答案 → 對照標準答案 → 給分與產生回饋
```

---

## ✅ 步驟與技術建議

### 1. 📄 **檔案格式建議**

* **優先建議**：`PDF`（方便頁面分割、OCR 處理佳）
* 可接受格式：`JPG`、`PNG`（掃描後的照片也可）
* 若是線上平台直接作答，也可儲存成文字（JSON/CSV 形式更易處理）

---

### 2. 🧠 **OCR 模組建議**

* 若輸入為圖檔或 PDF，先進行文字擷取
* 工具推薦：

  * **Tesseract OCR**（開源穩定）
  * **TrOCR（Transformers-based）**：效果較好，適合手寫字或掃描品質不佳的狀況
  * 若是純 PDF 文字層（非掃描圖像），可直接使用 `PyMuPDF` 或 `pdfplumber` 萃取文字，無需 OCR

---

### 3. 📊 **答案理解與評分模型**

* 你有「預設答案」，可以使用以下策略：

#### 評分方式選擇：

| 模式     | 技術                            | 優點           | 缺點               |
| ------ | ----------------------------- | ------------ | ---------------- |
| 關鍵字比對  | 手寫規則 / fuzzy match            | 快速、好控        | 無法處理同義句          |
| 語意比對   | Sentence-BERT / GPT Embedding | 能理解不同說法      | 須標準化答案           |
| LLM 評分 | GPT + 評分 Rubric               | 可產生自然評語、部分給分 | API 成本較高，需控制回答長度 |

#### 給分策略建議：

* 你可為每題設計 Rubric，如：

  * 主旨正確 +2 分
  * 用詞合理 +1 分
  * 補充細節 +1 分
  * 錯誤或答非所問 -1 分

這樣就可以把問題、學生答案、標準答案丟給 LLM 並請它依照 rubric 給出：

```markdown
得分：3 / 4
理由：主旨正確、用詞合理，但缺乏補充細節。
```

---

### 4. 🏗 建議技術架構（前期可簡化成 CLI 工具）

| 組件     | 技術選擇                                   |
| ------ | -------------------------------------- |
| 圖檔轉文字  | Python + Tesseract / TrOCR             |
| PDF 解析 | `pdfplumber`, `PyMuPDF`                |
| 答案比對   | 自訂關鍵字比對 or 使用 `sentence-transformers`  |
| 高階語意理解 | OpenAI GPT-4o / Claude / Mistral 等 LLM |
| 評分介面   | Python CLI / Flask / Streamlit （階段性進化） |

---

### 5. 📂 資料與範例建構（你可以這樣設計 dataset）

範例輸入格式（CSV/JSON）：

```json
{
  "question_id": "Q1",
  "question": "Explain the significance of the Boston Tea Party.",
  "student_answer": "It was a protest against British tea taxes.",
  "reference_answer": "The Boston Tea Party was a political protest against the Tea Act...",
  "rubric": {
    "mentions protest": 1,
    "mentions Tea Act": 1,
    "mentions American revolution context": 1,
    "provides clear explanation": 1
  }
}
```

然後讓模型依據 rubric 給分。

---

## 🔚 小結：初期開發路線圖

1. ✅ 先選好檔案格式：使用 PDF 最方便
2. ✅ 做基本 OCR（先用 Tesseract 測試）
3. ✅ 收集一些真實的英文問答題與答案樣本
4. ✅ 建立幾個評分 rubric（例如 3–5 題）
5. ✅ 接入 GPT 或 Sentence-BERT 評分測試
6. ✅ 將流程做成 Python 工具（可 CLI 或 Streamlit）

---

