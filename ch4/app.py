from search import answer_question

# 먼저 메시지 표시하기
print("질문을 입력하세요")

conversation_history = []

while True:
    # 사용자가 입력한 문자를 'user_input' 변수에 저장
    user_input = input()

    # 사용자가 입력한 문자가 'exit'인 경우 루프에서 빠져나옴
    if user_input == "exit":
        break
    
    conversation_history.append({"role": "user", "content": user_input})
    answer = answer_question(user_input, conversation_history)

    print("ChatGPT:", answer)
    conversation_history.append({"role": "assistant", "content":answer})
