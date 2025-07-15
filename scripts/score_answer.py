import json
from pathlib import Path

from sentence_transformers import SentenceTransformer, util # noqa: F401

# ── Paths ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent           # …/scripts
ROOT_DIR = BASE_DIR.parent                           # project root
RUBRIC_PATH = ROOT_DIR / "rubrics" / "rubric_Q1.json"
STUDENT_PATH = ROOT_DIR / "extracted_texts" / "student1.txt"
RESULT_DIR = ROOT_DIR / "results"
RESULT_PATH = RESULT_DIR / "student1_score.json"

# make sure results folder exists
RESULT_DIR.mkdir(parents=True, exist_ok=True)

# ── Model ────────────────────────────────────────────────────────────────
model = SentenceTransformer("all-MiniLM-L6-v2") # for sentence similarity

# ── Scoring logic ────────────────────────────────────────────────────────

def score(student_answer: str, rubric: dict): # 這裡 rubric 的類型提示可能需要更精確，但 dict 泛型足以
    """Simple keyword/phrase matching score with OR logic for keywords.

    `rubric` 的結構預期為 {"rule_name": {"keywords": List[str], "points": int}}.
    如果學生答案包含 `keywords` 列表中的任一關鍵字，則根據 `points` 計分。
    """
    total = 0
    feedback: list[str] = []
    lower_ans = student_answer.lower()

    # 遍歷 rubric 中的每個評分項目 (例如 "process", "plants")
    for rule_name, rule_details in rubric.items():
        keywords_to_match = rule_details["keywords"] # 獲取關鍵字列表
        point = rule_details["points"]               # 獲取這個評分點的分數

        matched = False
        matched_keyword = "" # 用於記錄匹配到的關鍵字，以便回饋
        for keyword in keywords_to_match:
            if keyword.lower() in lower_ans:
                matched = True
                matched_keyword = keyword # 記錄下來
                break # 只要找到一個符合的關鍵字就夠了

        if matched:
            total += point # 現在 point 是一個整數了！
            feedback.append(f"✔ 包含 '{matched_keyword}' (來自 '{rule_name}' 項目)")
        else:
            # 為了回饋訊息的可讀性，將所有關鍵字顯示出來
            feedback.append(f"✘ 缺少關鍵字於 '{rule_name}' 項目 (需包含任一: {', '.join(keywords_to_match)})")

    return total, feedback


# ── Load inputs ───────────────────────────────────────────────────────────
with RUBRIC_PATH.open(encoding="utf-8") as f:
    data = json.load(f)

with STUDENT_PATH.open(encoding="utf-8") as f:
    student_answer = f.read()

# ── Run scoring ──────────────────────────────────────────────────────────
score_val, fb = score(student_answer, data["rubric"])

# 計算 max_score 也要跟著改變
max_score = sum(rule_details["points"] for rule_details in data["rubric"].values())

result = {
    "student_id": "student1",
    "question_id": data["question_id"],
    "score": score_val,
    "max_score": max_score, # 使用新的 max_score 計算方式
    "feedback": " / ".join(fb),
}

# ── Save results ─────────────────────────────────────────────────────────
with RESULT_PATH.open("w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("✅ Scoring complete →", RESULT_PATH.relative_to(ROOT_DIR))