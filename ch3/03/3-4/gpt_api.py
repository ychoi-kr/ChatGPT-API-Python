# ライブラリ「openai」の読み込み
import openai
import os
# OpenAIのAPIキーを設定
openai.api_key = os.environ["OPENAI_API_KEY"]

# ChatGPTにリクエストを送信する関数を定義
def make_tweet():
    # ChatGPTに対する命令文を設定
    request = "私はIT関係の企業に勤める入社一年目の新入社員です。私に代わってTwitter投稿するツイートを140字以内で作成してください。\n\nツイートを作成する際は、以下の文を参考にしてください。\n\n"
    # 例文として与える投稿文を設定
    tweet1 = "例文1：仕事でPythonを使うことになりそうだから、現在勉強中！プログラミグとか難しくてよくわからないよ...\n\n"

    tweet2 = "例文2：最近ChatGPTについていろいろ調べてるんだけど、あれってなんでも質に答えてくれてすごいよね！とりあえずPythonを使って、簡単な会話をするプログラムをいてみるつもり。うまくできるかな？\n\n "

    # 文章を連結して一つの命令文にする
    content = request + tweet1 + tweet2

    # ChatGPTにリクエストを送信
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": content},
        ],
    )

    # 投稿文の内容を返却
    return response.choices[0]["message"]["content"]