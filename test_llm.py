from openai import OpenAI

# 連接到本機 LM Studio
client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

# 呼叫我們剛剛載入的 Qwen3 4B
response = client.chat.completions.create(
    model="qwen/qwen3-4b-2507",
    messages=[
        {
            "role": "user",
            "content": "請用繁體中文回答：什麼是 AI Agent？只用一句話回答。"
        }
    ],
    temperature=0
)

# 印出 LLM 的回答
print(response.choices[0].message.content)
