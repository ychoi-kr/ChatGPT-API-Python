import tweepy
import os

# Twitter APIキーを環境変数から取得
consumerKey = os.environ["TWITTER_CONSUMER_KEY"]
consumerSecret = os.environ["TWITTER_CONSUMER_SECRET"]
accessToken = os.environ["TWITTER_ACCESS_TOKEN"]
accessTokenSecret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
bearerToken = os.environ["TWITTER_BEARER_TOKEN"]

# ポストを投稿する関数を定義
def post(tweet):
    #tweepy クライアントを作成
    client = tweepy.Client(
        bearerToken,
        consumerKey,
        consumerSecret,
        accessToken,
        accessTokenSecret
    )

    # ポストを投稿
    client.create_tweet(text=tweet)