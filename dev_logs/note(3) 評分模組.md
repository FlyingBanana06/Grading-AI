# 2025-07-14

---

## ✅ 下一步建議：**實作答案理解與評分模組（MVP）**

這部分是整個自動閱卷系統的核心，重點是讓程式具備「看懂學生答案並評分」的能力。

---

### 🪜 分階段開發（推薦路線）

---

### **Step 1：建立「Rubric 檔案」 + 模板測資**

* 在 `rubrics/` 建立題目設定：

  ```json
  {
    "question_id": "Q1",
    "question": "What is photosynthesis?",
    "reference_answer": "Photosynthesis is the process by which plants convert light energy into chemical energy.",
    "rubric": {
      "mentions process": 1,
      "mentions plants": 1,
      "mentions light energy": 1,
      "mentions chemical energy": 1
    }
  }
  ```
* 在 `extracted_texts/` 模擬一個學生答案（txt/json 都可）：

  ```
  It is the process used by plants to change sunlight into food.
  ```

---

### **Step 2：寫一支 `score_answer.py` 腳本**

基本功能：

* 讀入：Rubric + 學生答案
* 使用簡單關鍵字比對 or 語意相似度（如 sentence-transformers）
* 輸出評分 json 到 `results/`：

```json
{
  "student_id": "student1",
  "question_id": "Q1",
  "score": 3,
  "max_score": 4,
  "feedback": "提到了植物、過程與光能，但缺少化學能的描述。"
}
```

---

### **Step 3：嘗試接 GPT 或 LLM API 做語意評分（可選）**

用 OpenAI GPT-4o（或 Claude）實驗：

```python
prompt = f"""
請根據以下 rubric 對學生答案評分：
題目：{question}
標準答案：{reference}
rubric：{rubric}
學生答案：{student_answer}
請回傳 json 格式，如：
{{"score": 3, "max_score": 4, "feedback": "..."}}。
"""
```

---

## 🔧 建議技術實作（Python 檔案）

```python
# scripts/score_answer.py

import json
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')  # for sentence similarity

def score(student_answer, rubric):
    score = 0
    feedback = []
    for rule, point in rubric.items():
        if rule in student_answer.lower():  # or use semantic match here
            score += point
            feedback.append(f"✔ 包含 {rule}")
        else:
            feedback.append(f"✘ 缺少 {rule}")
    return score, feedback

# Load inputs
with open('../rubrics/rubric_Q1.json') as f:
    data = json.load(f)

with open('../extracted_texts/student1.txt') as f:
    student_answer = f.read()

# Scoring
score_val, feedback = score(student_answer, data['rubric'])
result = {
    "student_id": "student1",
    "question_id": data["question_id"],
    "score": score_val,
    "max_score": sum(data['rubric'].values()),
    "feedback": " / ".join(feedback)
}

with open('../results/student1_score.json', 'w') as f:
    json.dump(result, f, indent=2)
```

---

### 🏁 完成這一步後，你會有：

* 一組簡單的題目、rubric、學生答案資料
* 一個可執行的「自動評分模組」
* 清楚的輸出格式（可再加分數統計、錯誤分析等）

---

如果你想再往下做，下一步可以是：

* 加入 Streamlit/Gradio 做成簡易介面
* 圖像切割（切出各題區塊，對應題號）
* 多學生批改 + 批次匯出成績