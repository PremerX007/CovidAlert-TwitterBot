import logging
import azure.functions as func
import requests
import tweepy
import pytz
from datetime import datetime
from ..shared import api

def main(mytimer: func.TimerRequest) -> None:
    if mytimer.past_due:
        logging.info('The timer is past due!')
    
    # Get Data From MOPH API
    url = "https://covid19.ddc.moph.go.th/api/Cases/today-cases-all"
    data_all = requests.get(url).json()[0]
    logging.info("[REQUESTS] Data received.")

    # Setting Time&Date
    bangkok_tz = pytz.timezone("Asia/Bangkok")
    th_time = datetime.now(bangkok_tz)
    date_now = th_time.strftime("%Y-%m-%d")

    # Twiiter Auth
    auth = tweepy.OAuthHandler(api.API_KEY, api.API_SECRET_KEY)
    auth.set_access_token(api.ACCESS_TOKEN, api.SECRET_ACCESS_TOKEN)
    logging.info("[TWEEPY] Connecting to Twiiter API >> @covidth_alert")
    API = tweepy.API(auth)
    logging.info("[TWEEPY] Connected!!")

    # Fecth Tweeted Timeline
    logging.info("[TWEEPY] Fecthing Tweeted Timeline")
    data_tweets = API.user_timeline(user_id=api.TWITTER_ID, count=1)
    for tweet in data_tweets:
        date_tweeted_fecth = str(tweet.created_at)[:-15]

    if data_all['txn_date'] == date_now and date_tweeted_fecth != date_now:
        # Get Tranding Hashtag in TH
        logging.info("[TWEEPY] Get Tranding Hasttag")
        woeid = 23424960 # number of WOEID (Where On Earth IDentifier) of Thailand
        trends = API.get_place_trends(id = woeid)
        result_trends = trends[0]["trends"]
        hashtags = [trend['name'] for trend in result_trends if "#" in trend['name']]

        # TwitterUpdateStatus
        show_date = th_time.strftime("%d/%m/%Y")
        daily_case = str(("🚨 ติดเชื้อใหม่ " + str(data_all["new_case"]) + " คน ❗\n")*3)
        daily_deaths = str(("⚠ เสียชีวิต " + str(data_all["new_death"]) + " คน\n")*3)
        timeline = str("📅 ณ วันที่ " + show_date + " 📅\n \n" + daily_case + daily_deaths + "#โควิดวันนี้ #โควิด19 " + hashtags[0] + " " + hashtags[1] + "\n \n" + "ddc.moph.go.th/covid19-dashboard")
        API.update_status(timeline)
        logging.info("[TWEEPY] Twitter tweeted status at %s", show_date)

        # line notify
        line_url = 'https://notify-api.line.me/api/notify'
        HEADERS = {'Authorization': 'Bearer ' + api.LINE_TOKEN}
        line_info_timenow = th_time.strftime("%d-%m-%Y" + '@' + "%H:%M")
        msg = line_info_timenow + " [INFO] Script Working!! : Microsoft Azure Serverless" 
        response = requests.post(line_url,headers=HEADERS,params={"message": msg})
        logging.info("[REQUESTS] LINE Notify : %s", response)
    elif date_tweeted_fecth != date_now:
        logging.info("[IDLE] Wait for new data from API.")
    else:
        logging.info("[IDLE] Today has already tweeted data.")