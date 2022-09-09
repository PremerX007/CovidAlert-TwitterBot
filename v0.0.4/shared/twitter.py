import tweepy
import logging

# All Twitter Keys
api_key = "**** private ****"
api_secret_key = "**** private ****"
access_token = "**** private ****"
secret_acess_token = "**** private ****"
twitter_id = '**** private ****'

def APIAuth(): # API Auth
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, secret_acess_token)
    logging.info("[APIAuth] Connecting to Twiiter API >> @covidth_alert")
    api = tweepy.API(auth)
    logging.info("[APIAuth] Connected!!")
    return api

def FecthLastestTweet(api, func : bool = False): # Fecth Tweeted Timeline
    user_id = 1419691747714605057
    data_tweets = api.user_timeline(user_id=user_id, count=1)
    for tweet in data_tweets:
        if func:
            logging.info("[FecthLastestTweet] Fecthing Tweeted Timeline")
            index = str(tweet.created_at)[:-15]
        else:
            index = int(tweet.id)
    return index

def tweet_msg(msg,api,reply_id=None):
    api.update_status(msg,in_reply_to_status_id=reply_id)

# if __name__ == '__main__':
#     a=FecthLastestTweet(api=APIAuth()) #Test Panels
#     logging.info(a)