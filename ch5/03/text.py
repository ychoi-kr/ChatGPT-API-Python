import openai
file = open("sample.wav", "rb")

transcript = openai.Audio.transcribe(
    model="whisper-1",
    file=file,
)

print(transcript.text) #結果を表示