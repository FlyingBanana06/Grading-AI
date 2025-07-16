# 2025-07-13

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

---

## 📄 PDF OCR Python 範例程式（`scripts/pdf_ocr.py`）

這裡用 **PyMuPDF**（處理 PDF）搭配 **Tesseract OCR**。

### 🔧 安裝需求：

```bash
pip install pytesseract pdf2image pillow
sudo apt install tesseract-ocr   # Linux 用戶才需要
```

Windows 用戶還需下載 [Tesseract OCR 安裝檔](https://github.com/tesseract-ocr/tesseract/wiki)。

---

## 🧪 測試方法

1. 把 `student1.pdf` 放進 `input_files/`
2. 執行指令：

   ```bash
   python scripts/pdf_ocr.py
   ```
3. 你會在 `extracted_texts/student1.txt` 看到 OCR 結果。

---