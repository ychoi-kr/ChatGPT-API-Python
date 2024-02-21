import pandas as pd
import tiktoken
from openai.embeddings_utils import get_embedding

embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"
max_tokens = 1500

# 「scraped.csv」ファイルを読み込み、カラム名を「title」と「text」に変更
df = pd.read_csv("scraped.csv")
df.columns = ['title', 'text']

tokenizer = tiktoken.get_encoding(embedding_encoding)
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
def split_into_many (text, max_tokens = 500):

    # テキストを文ごとに分割し、各文のトークン数を取得
    sentences = text.split('。')
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]

    chunks = []
    tokens_so_far = 0
    chunk = []

    # 各文とトークンを組み合わせてループ処理
    for sentence, token in zip(sentences, n_tokens):

        # これまでのトークン数と現在の文のトークン数を合計した値が
        # 最大トークン数を超える場合は、チャンクをチャンクのリストに追加し、
        # チャンクとトークン数をリセット
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        # 現在の文のトークン数が最大トークン数より大きい場合は、次の文へ進む
        if token > max_tokens:
            continue

        # それ以外の場合は、文をチャンクに追加し、トークン数を合計に追加
        chunk.append(sentence)
        tokens_so_far += token + 1

    # 最後のチャンクをチャンクのリストに追加
    if chunk:
        chunks.append(". ".join(chunk) + ".")
    return chunks
# 短縮されたテキストを格納するためのリスト
shortened = []

# DataFrameの各行に対してループ処理
for row in df.iterrows():
    # テキストがNoneの場合は、次の行へ進む
    if row[1]['text'] is None:
        continue
    # トークン数が最大トークン数より大きい場合は、テキストを
    # 「shortened」リストに追加
    if row[1]['n_tokens'] > max_tokens:
        shortened += split_into_many(row[1]['text'])

    # それ以外の場合は、テキストをそのまま「shortened」リストに追加
    else:
        shortened.append(row[1]['text'])

# 「shortened」をもとに新しいDataFrameを作成し、列名を「text」とする
df = pd.DataFrame(shortened, columns = ['text'])

# 各「text」のトークン数を計算し、新しい列「n_tokens」に格納
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

# 「text」列のテキストに対してembeddingを行い、CSVファイルに保存
df["embeddings"] = df.text.apply(lambda x: get_embedding(x,engine=embedding_model))
df.to_csv('embeddings.csv')