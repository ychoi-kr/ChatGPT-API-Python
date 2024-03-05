from openai import OpenAI
client = OpenAI()

response = client.moderations.create(
    input="안녕하세요!"
)
output = response.model_dump_json(indent=2)

print(output)