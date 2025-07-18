from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gpt_score(question, reference_answer, rubric, student_answer):
    prompt = f"""
你是一位老師，請根據下列題目與評分標準，評分學生答案並提供簡要回饋。

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
  "feedback": "<簡要評語>"
}}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 或 gpt-3.5-turbo 以節省成本 # 或 gpt-4o
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    reply = response.choices[0].message.content
    return json.loads(reply)
