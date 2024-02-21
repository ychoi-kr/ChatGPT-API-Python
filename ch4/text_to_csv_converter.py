import pandas as pd
# 正規表現を扱うためのライブラリ
import re

def remove_newlines(text):
    """
    文字列内の改行と連続する空白を削除する関数
    """
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r' +', ' ', text)
    return text

def text_to_df(data_file):
    """
    #テキストファイルを処理してDataFrameを返す関数
    """
    # テキストを格納するための空のリストを作成
    texts = []

    # 指定されたファイル（data_file）を読み込み、変数「file」に格納
    with open(data_file, 'r', encoding="utf-8") as file:
        # ファイルの内容を文字列として読み込む
        text = file.read()
        # 改行2つで文字列を分割
        sections = text.split('\n\n')

        # 各セクションに対して処理を行う
        for section in sections:
            # セクションを改行で分割する
            lines = section.split('\n')
            # 「lines」リストの最初の要素を取得
            fname = lines[0]
            # 「lines」リストの2番目以降の要素を取得
            content = ' '.join(lines[1:])
            # 「fname」と「content」をリストに追加
            texts.append([fname, content])

    # リストからDataFrameを作成
    df = pd.DataFrame(texts, columns=['fname', 'text'])
    # 「text」列内の改行を削除
    df['text'] = df['text'].apply(remove_newlines)

    return df

df = text_to_df('data.txt')
# 「scraped.csv」ファイルに書き込む
df.to_csv('scraped.csv', index=False, encoding='utf-8')