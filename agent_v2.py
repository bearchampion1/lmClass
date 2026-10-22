
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
# 2. 呼叫 Local LLM
# ============================================================

def ask_llm(messages):
    response = client.chat.completions.create(
        model="qwen/qwen3-4b-2507",
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content.strip()


# ============================================================
# 3. 使用者輸入
# ============================================================

question = input("請問問題：")


# ============================================================
# 4. 建立 Messages
# ============================================================

messages = [
    {
        "role": "system",
        "content": """
你是一個 Campus Agent。

目前可以查詢：
AI
Database
Network

如果使用者需要查詢課程資訊，
請回答：

COURSE:課程名稱

如果不需要查詢課程，
請回答：

FINAL

你是一個 Campus Agent。

目前可以查詢：
AI
Database
Network

如果需要查詢課程資料，請回答：
COURSE:課程名稱

每次只能查詢一門課程。

如果已經取得足夠的資料，可以回答使用者，
請回答：
FINAL

每次只能輸出一個指令。
不要加入其他文字。

"""
    },
    {
        "role": "user",
        "content": question
    }
]


# ============================================================
# 5. Agent Loop
# ============================================================

step = 0
max_steps = 3

while step < max_steps:

    step += 1

    print()
    print("========== Agent Step", step, "==========")

    # LLM Decision
    decision = ask_llm(messages)

    print("LLM Decision:", decision)

    # 結束條件
    if decision == "FINAL":
        print("Agent Finished")
        break

        # ============================================================
    # Tool Execution + Observation
    # ============================================================

    if decision.startswith("COURSE:"):

        course = decision.split(":", 1)[1].strip()

        # 執行真正的 Campus Tool
        result = get_course_info(course)

        print("Tool:", "get_course_info")
        print("Observation:", result)

        # 記錄 LLM 的 Decision
        messages.append({
            "role": "assistant",
            "content": decision
        })

        # 將真正的 Observation 交回 LLM
        messages.append({
            "role": "user",
            "content": f"""
    Observation:
    {result}

    請根據目前取得的資料，判斷是否還需要查詢其他課程。
    如果資料已經足夠，請回答 FINAL。
    """
        })

    else:
        print("無法辨識的 Decision:", decision)
        break

else:
    print("Agent 已達最大執行次數")
