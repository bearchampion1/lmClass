from openai import OpenAI
from campus_db import get_course_info


# 連接 LM Studio
client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)


# 呼叫 Local LLM
def ask_llm(messages):
    response = client.chat.completions.create(
        model="qwen/qwen3-4b-2507",
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content.strip()


# 取得使用者問題
question = input("請問問題：")


# 請 LLM 判斷下一步
decision_messages = [
    {
        "role": "system",
        "content": """
你是一個 Campus Agent。

你可以使用課程查詢工具。

目前支援的課程：
AI
Database
Network

規則：

如果使用者詢問課程的時間、教室或老師，
只能回答：

COURSE:課程名稱

例如：
COURSE:AI

如果問題與課程資訊無關，
只能回答：

ANSWER

不要加入任何其他文字。
"""
    },
    {
        "role": "user",
        "content": question
    }
]


# LLM 做 Decision
decision = ask_llm(decision_messages)

print("LLM Decision:", decision)


# Python 根據 Decision 執行 Tool
if decision.startswith("COURSE:"):

    course = decision.split(":", 1)[1].strip()

    print("Course:", course)

    result = get_course_info(course)

    print("Tool Result:", result)

else:

    print("這個問題不需要使用課程查詢工具。")
