import openai

response = openai.Moderation.create(
    input="こんにちは！"
)
output = response["results"][0]

print(output)