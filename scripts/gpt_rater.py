import openai
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt_score(question, reference_answer, rubric, student_answer):
    prompt = f"""
你是一位高中老師，請根據下列題目與評分標準，評分學生答案並提供簡要回饋。

題目：{question}

標準答案：{reference_answer}

評分標準（rubric）：
{json.dumps(rubric, ensure_ascii=False, indent=2)}

學生答案：
{student_answer}

請以 JSON 格式輸出，如下：
{{
  "score": <得分>,
  "max_score": <總分>,
  "feedback": "<給學生的簡要評語>"
}}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",  # 或 gpt-3.5-turbo 以節省成本
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    reply = response["choices"][0]["message"]["content"]
    return json.loads(reply)
