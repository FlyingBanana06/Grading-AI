# Grading-AI
一個提供自動閱卷功能的AI。An AI that for automatic paper marking. 


---

## 🗂 建議檔案結構（初期原型用）

```
grading_ai_project/
├── input_files/                # 放 PDF 試卷或學生答案
│   └── student1.pdf
├── extracted_texts/           # OCR 結果儲存成 txt 或 json
│   └── student1.txt
├── rubrics/                   # 每題的標準答案與評分標準
│   └── rubric_Q1.json
├── scripts/                   # Python 腳本放這裡
│   └── pdf_ocr.py
├── results/                   # 批改結果存這裡
│   └── student1_score.json
└── README.md
```

## 環境需求

- Python 3.x
- pip install -r requirements.txt
- apt install tesseract-ocr

---
