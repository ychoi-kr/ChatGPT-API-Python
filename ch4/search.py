import pandas as pd
from openai import OpenAI
import numpy as np
from typing import List
from scipy import spatial

client = OpenAI()

def create_context(question, df, max_len=1800):
    """
        질문과 학습 데이터를 비교해 컨텍스트를 만드는 함수
    """

    # 질문을 벡터화
    q_embeddings = client.embeddings.create(input=[question], model='text-embedding-3-small').data[0].embedding

    # 질문과 학습 데이터와 비교하여 코사인 유사도를 계산하고
    # 'distances' 열에 유사도를 저장
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].apply(eval).apply(np.array).values, distance_metric='cosine')
    
    # 컨텍스트를 저장하기 위한 리스트
    returns = []
    # 컨텍스트의 현재 길이
    cur_len = 0

    # 학습 데이터를 유사도 순으로 정렬하고 토큰 개수 한도까지 컨텍스트에
    # 추가
    for _, row in df.sort_values('distances', ascending=True).iterrows():
        # 텍스트 길이를 현재 길이에 더하기
        cur_len += row['n_tokens'] + 4

        # 텍스트가 너무 길면 루프 종료
        if cur_len > max_len:
            break

        # 컨텍스트 목록에 텍스트 추가하기
        returns.append(row["text"])

    # 컨텍스트를 결합해 반환
    return "\n\n###\n\n".join(returns)

def answer_question(question, conversation_history):
    """
    문맥에 따라 질문에 답하는 기능
    """

    # 학습 데이터 불러오기
    df = pd.read_csv('embeddings.csv')

    context = create_context(question, df, max_len=200)  #←질문과 학습 데이터를 비교해 컨텍스트 생성
    # 프롬프트를 생성하고 대화 기록에 추가하기
    prompt = f"당신은 어느 호텔 직원입니다. 문맥에 따라 고객의 질문에 정중하게 대답해 주십시오. 컨텍스트가 질문에 대답할 수 없는 경우 '모르겠습니다'라고 대답하세요.\n\n컨텍스트: {context}\n\n---\n\n질문: {question}\n답변:"
    conversation_history.append({"role": "user", "content": prompt})

    try:
        # ChatGPT에서 답변 생성
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            temperature=1,
        )

        # ChatGPT에서 답변 반환
        return response.choices[0].message.content.strip()
    except Exception as e:
        # 오류가 발생하면 빈 문자열을 반환
        print(e)
        return ""
    
# 각 문장의 토큰 수를 계산하여 새로운 열 'n_tokens'에 저장(옮긴이가 추가함)
def distances_from_embeddings(
    query_embedding: List[float],
    embeddings: List[List[float]],
    distance_metric="cosine",
) -> List[List]:
    """Return the distances between a query embedding and a list of embeddings."""
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    return distances