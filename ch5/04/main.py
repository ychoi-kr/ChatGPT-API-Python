import openai

file = open("sample.wav", "rb")

transcript = openai.Audio.transcribe(
    model="whisper-1",
    file=file,
)
# 챗GPT로 요약하기
summary = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": f"다음 문장을 3줄의 글머리 기호로 요약해 주세요:\n{transcript}"
        }
    ]
)

print(summary.choices[0].message.content)
