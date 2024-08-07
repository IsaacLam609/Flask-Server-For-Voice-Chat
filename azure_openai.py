from openai import AzureOpenAI
import azure_key

client = AzureOpenAI(
  azure_endpoint=azure_key.OPENAI_ENDPOINT,
  api_key=azure_key.OPENAI_KEY,
  api_version="2024-02-01"
)

response = client.chat.completions.create(
    model="test-gpt-35-turbo",                  # deployment name
    messages=[
        {"role": "system", "content": "你是一個獨居老人的智慧家居助手。你的主要功能是操控智慧家居的裝置。在控制裝置前記得先向用家確認"},
        {"role": "user", "content": "我而家有啲悶"},
        {"role": "assistant", "content": "不要擔心，您需要聊聊天嗎？我可以陪伴您聊天和解悶，甚至幫您查詢一些資訊。我們也可以聊聊您生活中的趣事、回憶或者未來的計劃。"},
        {"role": "user", "content": "我嘅仔女好耐無嚟探我"}
    ]
)

print(response.choices[0].message.content)

