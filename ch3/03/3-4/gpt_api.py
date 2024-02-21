# openai 라이브러리 불러오기
import openai
import os
# OpenAI의 API 키 설정
openai.api_key = os.environ["OPENAI_API_KEY"]

# 챗GPT에 요청을 전송하는 함수 정의
def make_tweet():
    # 챗GPT에 대한 명령문 설정
    request = "저는 IT 관련 기업에 근무하는 입사 1년차 신입사원입니다. 저를 대신해 트위터에 올릴 트윗을 140자 이내로 작성해 주세요. n\n\n 트윗을 작성할 때 다음 예문을 참고해 주세요.\n\n"
    # 예문으로 줄 포스팅 문장 설정
    tweet1 = "예문1: 직장에서 파이썬을 사용하게 될 것 같아서 현재 공부 중입니다! 프로그래밍이라든가 어려워서 잘 모르겠어...\n\n"

    tweet2 = "예문2: 최근에 ChatGPT에 대해 여러 가지를 알아보고 있는데, 어떤 질문에도 대답해줘서 정말 대단하네요! 일단 Python으로 간단한 대화를 하는 프로그램을 작성해 볼 생각이에요. 잘 할 수 있을까?\n\n "

    # 문장을 연결해 하나의 명령문으로 만들기
    content = request + tweet1 + tweet2

    # 챗GPT에 요청 보내기
    response = openai.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": content},
        ],
    )

    # 게시글 내용 반환
    return response.choices[0].message.content