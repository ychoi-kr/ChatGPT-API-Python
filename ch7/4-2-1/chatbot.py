from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain.indexes.vectorstore import VectorstoreIndexCreator

loader = PyPDFLoader("★ 서울특별시 스마트도시 및 정보화 기본계획(홈페이지 게시용).pdf")

index = VectorstoreIndexCreator(embedding=OpenAIEmbeddings()).from_loaders([loader])
print("질문을 입력하세요")
answer = index.query(input())
print(answer)
