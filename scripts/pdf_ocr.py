import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

# === 自動偵測目前路徑（適用 Codespace） ===
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.abspath(os.path.join(CURRENT_DIR, "..", "input_files"))
OUTPUT_FOLDER = os.path.abspath(os.path.join(CURRENT_DIR, "..", "extracted_texts"))

# === Debug 印出 ===
print("[DEBUG] Current script path:", CURRENT_DIR)
print("[DEBUG] Input folder path:", INPUT_FOLDER)
print("[DEBUG] Output folder path:", OUTPUT_FOLDER)

# === 主要函式 ===
def pdf_to_images(pdf_path):
    return convert_from_path(pdf_path, dpi=300)

def ocr_image(image):
    return pytesseract.image_to_string(image, lang='eng')

def extract_text_from_pdf(pdf_filename):
    pdf_path = os.path.join(INPUT_FOLDER, pdf_filename)

    if not os.path.exists(pdf_path):
        print(f"[✗] 找不到 PDF 檔案：{pdf_path}")
        return

    try:
        images = pdf_to_images(pdf_path)
    except Exception as e:
        print(f"[✗] PDF 轉換失敗：{e}")
        return

    all_text = ""
    for i, img in enumerate(images):
        text = ocr_image(img)
        all_text += f"\n--- Page {i+1} ---\n{text}\n"

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    output_path = os.path.join(OUTPUT_FOLDER, pdf_filename.replace(".pdf", ".txt"))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(all_text)

    print(f"[✓] OCR 完成，文字儲存至：{output_path}")

# === 主程式 ===
if __name__ == "__main__":
    extract_text_from_pdf("ocr_test.pdf")
