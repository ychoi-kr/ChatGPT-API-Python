import openai
file = open("sample.wav", "rb")

transcript = openai.Audio.transcribe(
    model="whisper-1",
    file=file,
)

print(transcript.text) # 결과를 표시