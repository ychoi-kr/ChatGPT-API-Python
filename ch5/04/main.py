import openai

file = open("sample.wav", "rb")

transcript = openai.Audio.transcribe(
    model="whisper-1",
    file=file,
)
# ChatGPTで要約する
summary = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": f"以下の文章を3行の箇条書きで要約してください:\n{transcript}"
        }
    ]
)

print(summary.choices[0].message.content)
