import openai

response = openai.Moderation.create(
    input="안녕하세요!"
)
output = response["results"][0]

print(output)