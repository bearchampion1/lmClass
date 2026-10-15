
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
max_steps = 5

# 記錄已經查詢過的課程
queried_courses = set()

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

        # 記錄 LLM 已決定結束查詢
        messages.append({
            "role": "assistant",
            "content": decision
        })

        # 建立最後回答的 Messages
        final_messages = messages + [
            {
                "role": "system",
                "content": """
    你現在要產生 Campus Agent 的最後答案。

    請根據之前取得的 Observation，
    回答使用者最初的問題。

    規則：
    1. 只能根據 Observation 提供的資料回答。
    2. 不可以編造課程資訊。
    3. 使用繁體中文。
    4. 回答簡短清楚。
    5. 不要輸出 COURSE 或 FINAL 指令。
    """
            },
            {
                "role": "user",
                "content": f"""
    原始問題：
    {question}

    請根據已經取得的課程資料，產生最後答案。
    """
            }
        ]

        # 再次呼叫 LLM 產生自然語言答案
        final_answer = ask_llm(final_messages)

        print()
        print("Final Answer:", final_answer)

        break


    # ============================================================
    # Tool Execution + Observation
    # ============================================================

    if decision.startswith("COURSE:"):

        course = decision.split(":", 1)[1].strip()
            # 如果已經查詢過，就不要重複執行 Tool
        if course in queried_courses:

            print("Duplicate Tool Call:", course)

            messages.append({
                "role": "assistant",
                "content": decision
            })

            messages.append({
                "role": "user",
                "content": f"""
    Observation:
    {course} 課程已經查詢過。

    請不要重複查詢相同課程。
    請根據原始問題與之前的 Observation，
    判斷是否還需要查詢其他課程。

    如果資料已足夠，請回答 FINAL。
    """
            })

            continue

        # 執行真正的 Campus Tool
        result = get_course_info(course)
            # 記錄這門課程已經查詢過
        queried_courses.add(course)

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

