import tweepy
from os import environ

# All Twitter Keys
api_key = environ.get("API_KEY")
api_secret_key = environ.get("API_SECRET_KEY")
access_token = environ.get("ACCESS_TOKEN")
access_token_secret = environ.get("SECRET_ACCESS_TOKEN")
user_id = environ.get("USER_ID")

def APIAuth(): # API Auth
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    print("[APIAuth] Connecting to Twiiter API >> @covidth_alert")
    api = tweepy.API(auth)
    print("[APIAuth] Connected!!")
    return api

def FecthLastestTweet(api, week : bool = False): # Fecth Tweeted Timeline
    data_tweets = api.user_timeline(user_id=user_id, count=1)
    for tweet in data_tweets:
        if week:
            print("[FecthLastestTweet] Fecthing Lastest Tweet Timeline (Weeknum)")
            index = int((tweet.text[:15])[13:15])
        else:
            index = int(tweet.id)
    return index

def Tweet_msg(msg,api,reply_id : int = None):
    api.update_status(msg,in_reply_to_status_id=reply_id)

if __name__ == '__main__':
    # FecthLastestTweet(api=APIAuth(),func=True) #Test Panels
    APIAuth().update_status("Testing On Product")