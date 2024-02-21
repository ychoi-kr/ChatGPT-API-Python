import pandas as pd
# 정규표현식을 다루기 위한 라이브러리
import re

def remove_newlines(text):
    """
    문자열의 줄 바꿈과 연속된 공백을 삭제하는 함수
    """
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r' +', ' ', text)
    return text

def text_to_df(data_file):
    """
    텍스트 파일을 처리하여 DataFrame을 반환하는 함수
    """
    # 텍스트를 저장할 빈 목록 만들기
    texts = []

    # 지정된 파일(data_file)을 읽어들여 변수 'file'에 저장
    with open(data_file, 'r', encoding="utf-8") as file:
        # 파일 내용을 문자열로 불러오기
        text = file.read()
        # 줄 바꿈으로 문자열을 두 줄로 나누기
        sections = text.split('\n\n')

        # 각 섹션에 대해 처리하기
        for section in sections:
            # 섹션을 줄 바꿈으로 나누기
            lines = section.split('\n')
            # "lines" 목록의 첫 번째 요소를 얻기
            fname = lines[0]
            # 'lines' 목록의 두 번째 이후 요소를 얻기
            content = ' '.join(lines[1:])
            # fname과 content를 리스트에 추가
            texts.append([fname, content])

    # 목록에서 DataFrame 생성
    df = pd.DataFrame(texts, columns=['fname', 'text'])
    # 'text' 열의 줄 바꿈 제거
    df['text'] = df['text'].apply(remove_newlines)

    return df

df = text_to_df('data.txt')  #←'data.txt'의 데이터를 처리
# 'scraped.csv' 파일에 쓰기
df.to_csv('scraped.csv', index=False, encoding='utf-8')