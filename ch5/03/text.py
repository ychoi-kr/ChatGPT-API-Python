import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]
client = openai.OpenAI()

file = open("sample.wav", "rb")

transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=file,
)

print(transcript.text) # 결과를 표시