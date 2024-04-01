from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Python에 대해 알려주세요"},
    ],
)
print(response.choices[0].message.content)
