import os
import openai
from search import answer_question

openai.api_key = os.environ["OPENAI_API_KEY"]

# 最初にメッセージを表示する
print("質問を入力してください")

conversation_history = []

while True:
    # ユーザーの入力した文字を変数「user_input」に格納
    user_input = input()

    # ユーザーの入力した文字が「exit」の場合はループを抜ける
    if user_input == "exit":
        break
    
    conversation_history.append({"role": "user", "content": user_input})
    answer = answer_question(user_input, conversation_history)

    print("ChatGPT:", answer)
    conversation_history.append({"role": "assistant", "content":answer})
