import os
import re
import json
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage


def extract_and_parse_json(text):
    """
    텍스트에서 JSON 문자열을 추출하여 사전형으로 변환하는 기능
    """
    try:
        # 'text'에서 JSON 문자열 추출하기
        match = re.search(r"\{.*\}", text, re.DOTALL)
        json_string = match.group() if match else ""
        # JSON 문자열을 파이썬의 딕셔너리형으로 변환
        return json.loads(json_string)
    except (AttributeError, json.JSONDecodeError):
        # 두 작업 중 하나라도 실패하면 빈 딕셔너리를 반환한다.
        return {}


def load_all_pdfs(directory):
    """
    directory 폴더 아래의 PDF 파일을 읽어와 JSON 형식의 데이터 배열을 반환하는 함수
    """
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0)
    
    # directory 폴더 내의 PDF 파일 목록을 얻음
    pdf_files = [f for f in os.listdir(directory) if f.endswith(".pdf")]
    
    # 각 PDF의 JSON을 저장할 배열을 정의
    contents = []
    
    for pdf_file in pdf_files:
        loader = PyPDFLoader(os.path.join(directory, pdf_file))
        pages = loader.load_and_split()
        prompt = f""""
        다음 데이터는 청구서 PDF 데이터를 텍스트로 변환한 것입니다.
        청구서 데이터를 다음의 키를 가진 JSON 형식으로 변환하세요.
        키에 해당하는 텍스트를 찾지 못하면 값을 비워둡니다.
        
        또한, 다음 내용은 당사 정보이므로 JSON 출력에 포함하지 마십시오.
         - AI 비즈니스 솔루션 주식회사
         - ㉾ 05500 서울특별시 송파구 올림픽로 1234번지 테크빌딩 789층
        
        ###
        
        키:
        - 발행일
        - 청구 번호
        - 인보이스 번호
        - 회사명
        - 주소
        - 제목
        - 청구 금액
        - 결제 기한
        - 상세 정보
        - 소계
        - 소비세
        - 청구금액(총액)
        - 송금처
        
        ###
        
        다음은 청구서 데이터를 JSON 형식으로 변환한 예시입니다.
        
        ###
        
        예:
        [(
            "날짜": "2023년 10월 31일",
            "청구 번호": "2023-1031"
            "인보이스 번호": "T0123456789012",
            "회사명": "테크놀로지 솔루션즈 주식회사"
            "주소": "㉾ 05500 서울특별시 송파구 올림픽로 1234번지 테크빌딩 789층",
            "제목": "웹사이트 리뉴얼 프로젝트",
            "청구 금액": "2,275,000",
            "지급 기한": "2023년 11월 30일"
            "상세": "디렉팅 비용 ₩1,000,000 / 개발 비용 ₩1,500,000",
            "소계": "2,500,000",
            "소비세": "250,000",
            "청구금액(총액)": "2,275,000",
            "입금처": "AA은행 BB지점 보통 1234567"
        )]
        
        ###
        
        데이터:
        {pages[0].page_content}
        """
        
        result = llm.invoke([HumanMessage(content=prompt)])
        
        contents.append(extract_and_parse_json(result.content))
    return contents
