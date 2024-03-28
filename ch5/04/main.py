from openai import OpenAI
client = OpenAI()

file = open("sample.wav", "rb")
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=file,
)

# 챗GPT로 요약하기
summary = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": f"다음 문장을 3줄의 글머리 기호로 요약해 주세요:\n{transcript}"
        }
    ]
)

print(summary.choices[0].message.content)
print(f"요약에 사용한 토큰 수: {summary.usage.total_tokens}")
