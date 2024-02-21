import gpt_api
import twitter_api

# 챗GPT에서 트윗 내용 가져오기
tweet = gpt_api.make_tweet()

# 트위터에 트윗을 올리기
twitter_api.post(tweet)