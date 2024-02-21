import openai
import os
openai.api_key = os.environ["OPENAI_API_KEY"]

file = open("sample.wav", "rb")

transcript = openai.Audio.translate(
    model="whisper-1",
    file=file,
)

# ChatGPTで要約する
summary = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": f"以下の文章を日本語に翻訳し、3行の箇条書きで要約してください:\n{transcript}"
        }
    ]
)

print(f"要約結果: \n{summary.choices[0].message.content}")
print(f"要約に使用したトークン数: {summary.usage.total_tokens}")
