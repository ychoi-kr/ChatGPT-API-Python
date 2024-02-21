import openai
import os
openai.api_key = os.environ["OPENAI_API_KEY"]

file = open("sample.wav", "rb")

transcript = openai.Audio.translate(
    model="whisper-1",
    file=file,
)

# ChatGPTで要約する
summary = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": f"다음 문장을 한국어로 번역하고 3줄의 글 머리 기호로 요약하세요:\n{transcript}"
        }
    ]
)

print(f"요약 결과: \n{summary.choices[0].message.content}")
print(f"요약에 사용한 토큰 수: {summary.usage.total_tokens}")
