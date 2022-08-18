import logging
import azure.functions as func
import requests
import tweepy
import pytz
from datetime import datetime


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')
    
    # Twiiter Auth
    auth = tweepy.OAuthHandler("*** API_KEY ***", "*** API_SECRET_KEY ***")
    auth.set_access_token("*** ACCESS_TOKEN ***", "*** SECRET_ACCESS_TOKE ***")
    logging.info("[!] Connecting to Twiiter API >> @covidth_alert")
    API = tweepy.API(auth)
    logging.info("[!] Connected!!")

    # Request JSON
    url = "https://covid19.ddc.moph.go.th/api/Cases/today-cases-all"
    data = requests.get(url).json()[0]

    # Get Tranding Hashtag in TH
    woeid = 23424960
    trends = API.get_place_trends(id = woeid)
    rs = trends[0]["trends"]
    hashtags = [trend['name'] for trend in rs if "#" in trend['name']]

    # TwitterUpdateStatus
    bangkok_tz = pytz.timezone("Asia/Bangkok")
    time_now = datetime.now(bangkok_tz).strftime("%d/%m/%Y")
    daily_case = str(("🚨 ติดเชื้อใหม่ " + str(data["new_case"]) + " คน ❗\n")*3)
    daily_deaths = str(("⚠ เสียชีวิต " + str(data["new_death"]) + " คน\n")*3)
    timeline = str("📅 ณ วันที่ " + time_now + " 📅\n \n" + daily_case + daily_deaths + "#โควิดวันนี้ #โควิด19 " + hashtags[0] + " " + hashtags[1] + "\n \n" + "ddc.moph.go.th/covid19-dashboard")
    API.update_status(timeline)
    logging.info("Tweeted @%s", time_now)

    # line notify
    line_url = 'https://notify-api.line.me/api/notify'
    line_token = '*** LINE_TOKEN ***' # Get this token from https://notify-bot.line.me
    HEADERS = {'Authorization': 'Bearer ' + line_token}
    line_info_timenow = datetime.now(bangkok_tz).strftime("%d-%m-%Y" + '@' + "%H:%M")
    msg = line_info_timenow + " [INFO] Script Working!! : Microsoft Azure Serverless\nUser:bannawat_v@cmu.ac.th" 
    response = requests.post(line_url,headers=HEADERS,params={"message": msg})
    logging.info(response)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
