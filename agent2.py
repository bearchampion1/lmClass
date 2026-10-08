from openai import OpenAI
from campus_db import get_course_info


# ============================================================
# 1. 連接 LM Studio
# ============================================================

client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)


# ============================================================
# 2. 建立呼叫 Local LLM 的函式
# ============================================================

def ask_llm(messages):
    response = client.chat.completions.create(
        model="qwen/qwen3-4b-2507",
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content.strip()


# ============================================================
# 3. 取得使用者問題
# ============================================================

question = input("請問問題：")


# ============================================================
# 4. 請 LLM 判斷下一步要做什麼
# ============================================================

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


# ============================================================
# 5. 第一次呼叫 LLM：讓 LLM 做 Decision
# ============================================================

decision = ask_llm(decision_messages)

print()
print("LLM Decision:", decision)


# ============================================================
# 6. 根據 LLM Decision 決定是否使用 Tool
# ============================================================

if decision.startswith("COURSE:"):

    # --------------------------------------------------------
    # 6-1. 從 COURSE:AI 取出 AI
    # --------------------------------------------------------

    course = decision.split(":", 1)[1].strip()

    print("Course:", course)


    # --------------------------------------------------------
    # 6-2. 執行 Campus Tool
    # --------------------------------------------------------

    result = get_course_info(course)

    print("Tool Result:", result)


    # --------------------------------------------------------
    # 6-3. 把 Tool 的 Observation 交回 LLM
    # --------------------------------------------------------

    final_messages = [
        {
            "role": "system",
            "content": """
你是一個 Campus Agent。

請根據提供的課程資料回答使用者問題。

只能根據提供的資料回答，
不要自己編造不存在的資訊。

請使用繁體中文簡短回答。
"""
        },
        {
            "role": "user",
            "content": f"""
使用者問題：
{question}

課程查詢結果：
{result}
"""
        }
    ]


    # --------------------------------------------------------
    # 6-4. 第二次呼叫 LLM：產生最後答案
    # --------------------------------------------------------

    final_answer = ask_llm(final_messages)

    print("Final Answer:", final_answer)


# ============================================================
# 7. 如果不需要使用 Campus Tool
# ============================================================

else:

    normal_messages = [
        {
            "role": "system",
            "content": """
你是一個 Campus Agent。

如果問題不需要查詢校園資料，
請直接回答使用者。

請使用繁體中文簡短回答。
"""
        },
        {
            "role": "user",
            "content": question
        }
    ]


    # 第二次呼叫 LLM，直接回答
    final_answer = ask_llm(normal_messages)

    print("Final Answer:", final_answer)
