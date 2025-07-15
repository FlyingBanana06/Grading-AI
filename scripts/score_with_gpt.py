import json
import os
from gpt_rater import gpt_score

# === 自動偵測當前腳本目錄 ===
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 絕對路徑
RUBRIC_PATH = os.path.join(CURRENT_DIR, "..", "rubrics", "rubric_Q1.json")
ANSWER_PATH = os.path.join(CURRENT_DIR, "..", "extracted_texts", "student1.txt")
OUTPUT_PATH = os.path.join(CURRENT_DIR, "..", "results", "student1_score_gpt.json")

# 讀取題目與評分規則
with open(RUBRIC_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# 讀取學生答案
with open(ANSWER_PATH, "r", encoding="utf-8") as f:
    student_answer = f.read()

# 呼叫 GPT 評分
result = gpt_score(
    question=data["question"],
    reference_answer=data["reference_answer"],
    rubric=data["rubric"],
    student_answer=student_answer
)

# 補上學生/題目 ID，並存到檔案
result["student_id"] = "student1"
result["question_id"] = data["question_id"]

# 儲存結果
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
