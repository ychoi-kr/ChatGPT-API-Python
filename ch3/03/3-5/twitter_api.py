import tweepy
import os

# 환경 변수에서 트위터 API 키 가져오기
consumerKey = os.environ["TWITTER_CONSUMER_KEY"]
consumerSecret = os.environ["TWITTER_CONSUMER_SECRET"]
accessToken = os.environ["TWITTER_ACCESS_TOKEN"]
accessTokenSecret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
bearerToken = os.environ["TWITTER_BEARER_TOKEN"]

# 게시물을 게시하는 함수 정의
def post(tweet):
    # tweepy 클라이언트 만들기
    client = tweepy.Client(
        bearerToken,
        consumerKey,
        consumerSecret,
        accessToken,
        accessTokenSecret
    )

    # 포스트 게시하기
    client.create_tweet(text=tweet)