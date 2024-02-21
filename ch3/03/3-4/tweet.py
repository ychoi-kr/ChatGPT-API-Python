import gpt_api
import twitter_api

# ChatGPTからツイート内容を取得
tweet = gpt_api.make_tweet()

# Twitterにツイートを投稿
twitter_api.post(tweet)