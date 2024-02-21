import os
import re
import json
from langchain.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


def extract_and_parse_json(text):
    """
    テキストからJSON文字列を抽出し、辞書型に変換する関数
    """
    try:
        # 「text」からJSON文字列を抽出する
        match = re.search(r"\{.*\}", text, re.DOTALL)
        json_string = match.group() if match else ""
        # JSON文字列をPythonの辞書型に変換
        return json.loads(json_string)
    except (AttributeError, json.JSONDecodeError):
        # どちらかの操作が失敗した場合は、空の辞書型を返す
        return {}


def load_all_pdfs(directory):
    """
    「directory」フォルダ以下のPDFファイルを読み込み、JSON形式のデータの配列を返す関数
    """
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.0)

    # 「directory」フォルダ以下のPDFファイルの一覧を取得
    pdf_files = [f for f in os.listdir(directory) if f.endswith(".pdf")]

    # 各PDFのJSONを格納する配列を定義
    contents = []

    for pdf_file in pdf_files:
        loader = PyPDFLoader(os.path.join(directory, pdf_file))
        pages = loader.load_and_split()
        prompt = f"""
        以下に示すデータは、請求書のPDFデータをテキスト化したものです。
        請求書データを、下記のキーを持つJSON形式に変換してください。
        キーに該当するテキストが見つからなければ、値は空欄にしてください。

        また、下記は弊社の情報なので、JSONの出力に含めないでください。
        ・AIビジネスソリューション株式会社
        ・〒135-0021 東京都江東区有明1-1-1

        ###

        キー：
        ・日付
        ・請求番号
        ・インボイス番号
        ・会社名
        ・住所
        ・件名
        ・請求金額
        ・お支払い期限
        ・詳細
        ・小計
        ・消費税
        ・請求金額（合計）
        ・振込先

        ###

        以下はとある請求書のデータをJSON形式に変換した場合の例です。

        ###

        例：
        [(
            "日付": "2023年10月31日",
            "請求番号": "2023-1031",
            "インボイス番号": "T0123456789012",
            "会社名": "テクノロジーソリューションズ株式会社",
            "住所": "〒123-4567 東京都中央区銀座1-1-1",
            "件名": "ウェブサイトリニューアルプロジェクト",
            "請求金額": "667,810",
            "お支払い期限": "2023年11月30日",
            "詳細": "ディレクション費用 ¥100,000 / 開発費用 ¥150,000",
            "小計": "250,000",
            "消費税": "25,000",
            "請求金額（合計）": "667,810",
            "振込先": "AA銀行 BB支店 普通 1234567"
        )]

        ###

        データ：
        {pages[0].page_content}
        """

        result = llm([HumanMessage(content=prompt)])

        contents.append(extract_and_parse_json(result.content))
    return contents

   
