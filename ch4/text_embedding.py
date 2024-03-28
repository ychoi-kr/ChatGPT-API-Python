import pandas as pd
import tiktoken
from openai import OpenAI
from typing import List

client = OpenAI()

embedding_model = "text-embedding-3-small"
embedding_encoding = "cl100k_base"
max_tokens = 1500

# 'scraped.csv' 파일을 불러와서 칼럼 이름을 'title'과 'text'로 변경
df = pd.read_csv("scraped.csv")
df.columns = ['title', 'text']

tokenizer = tiktoken.get_encoding(embedding_encoding)
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

def split_into_many (text, max_tokens = 500):

    # 텍스트를 문장별로 나누어 각 문장의 토큰 개수를 구함
    sentences = text.split('.')
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]

    chunks = []
    tokens_so_far = 0
    chunk = []

    # 각 문장과 토큰을 결합해 루프 처리
    for sentence, token in zip(sentences, n_tokens):

        # 지금까지의 토큰 수와 현재 문장의 토큰 수를 합한 값이
        # 최대 토큰 수를 초과하면 청크를 청크 목록에 추가하고
        # 청크 및 토큰 수를 재설정
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        # 현재 문장의 토큰 수가 최대 토큰 수보다 크면 다음 문장으로 넘어감
        if token > max_tokens:
            continue

        # 그렇지 않은 경우, 문장을 청크에 추가하고 토큰 수를 합계에 추가
        chunk.append(sentence)
        tokens_so_far += token + 1

    # 마지막 청크를 청크 목록에 추가
    if chunk:
        chunks.append(". ".join(chunk) + ".")
    return chunks

# 축약된 텍스트를 저장하기 위한 리스트
shortened = []

# DataFrame의 각 행에 대한 루프 처리
for row in df.iterrows():
    # 텍스트가 None인 경우 다음 줄로 넘어감
    if row[1]['text'] is None:
        continue
    # 토큰 수가 최대 토큰 수보다 큰 경우, 텍스트를
    # shortened 리스트에 추가
    if row[1]['n_tokens'] > max_tokens:
        shortened += split_into_many(row[1]['text'])

    # 그 외의 경우 텍스트를 그대로 'shortened' 목록에 추가
    else:
        shortened.append(row[1]['text'])

#"shortened"를 기반으로 새로운 DataFrame을 생성하고, 열 이름을 "text"로 지정
df = pd.DataFrame(shortened, columns = ['text'])

# 각 'text'의 토큰 수를 계산하여 새로운 열 'n_tokens'에 저장
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

# 'text' 열의 텍스트에 대해 embedding을 수행하여 CSV 파일로 저장(옮긴이가 추가함)
def get_embedding(text, model):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

#'text' 열의 텍스트에 대해 embedding을 수행하여 CSV 파일로 저장
df["embeddings"] = df.text.apply(lambda x: get_embedding(x, model=embedding_model))
df.to_csv('embeddings.csv')
