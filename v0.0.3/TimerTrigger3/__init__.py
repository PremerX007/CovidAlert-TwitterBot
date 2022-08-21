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
    
    # Request JSON
    url = "https://covid19.ddc.moph.go.th/api/Cases/today-cases-all"
    data_all = requests.get(url).json()[0]

    # Setting Time&Date
    bangkok_tz = pytz.timezone("Asia/Bangkok")
    th_time = datetime.now(bangkok_tz)

    # Twiiter Auth
    auth = tweepy.OAuthHandler(api.API_KEY, api.API_SECRET_KEY)
    auth.set_access_token(api.ACCESS_TOKEN, api.SECRET_ACCESS_TOKEN)
    logging.info("[!] Connecting to Twiiter API >> @covidth_alert")
    API = tweepy.API(auth)
    logging.info("[!] Connected!!")

    # Get Tranding Hashtag in TH
    woeid = 23424960 # number of WOEID (Where On Earth IDentifier) of Thailand
    trends = API.get_place_trends(id = woeid)
    result_trends = trends[0]["trends"]
    hashtags = [trend['name'] for trend in result_trends if "#" in trend['name']]

    # TwitterUpdateStatus
    time_now = th_time.strftime("%d/%m/%Y")
    daily_case = str(("🚨 ติดเชื้อใหม่ " + str(data_all["new_case"]) + " คน ❗\n")*3)
    daily_deaths = str(("⚠ เสียชีวิต " + str(data_all["new_death"]) + " คน\n")*3)
    timeline = str("📅 ณ วันที่ " + time_now + " 📅\n \n" + daily_case + daily_deaths + "#โควิดวันนี้ #โควิด19 " + hashtags[0] + " " + hashtags[1] + "\n \n" + "ddc.moph.go.th/covid19-dashboard")
    API.update_status(timeline)
    logging.info("Tweeted @%s", time_now)

    # line notify
    line_url = 'https://notify-api.line.me/api/notify'
    HEADERS = {'Authorization': 'Bearer ' + api.LINE_TOKEN}
    line_info_timenow = th_time.strftime("%d-%m-%Y" + '@' + "%H:%M")
    msg = line_info_timenow + " [INFO] Script Working!! : Microsoft Azure Serverless" 
    response = requests.post(line_url,headers=HEADERS,params={"message": msg})
    logging.info(response)
