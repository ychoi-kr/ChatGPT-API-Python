from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator

loader = PyPDFLoader("digital_01_202107_keikaku.pdf")

index = VectorstoreIndexCreator().from_loaders([loader])
print("質問を入力してください")
answer = index.query(input())
print(answer)