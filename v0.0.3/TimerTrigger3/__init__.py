import logging
import azure.functions as func
import requests
import tweepy
import pytz
import datetime


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
    r = requests.get(url).json()
    a = r[0]

    # Get Tranding Hashtag in TH
    woeid = 23424960
    trends = API.get_place_trends(id = woeid)
    rs = trends[0]["trends"]
    hashtags = [trend['name'] for trend in rs if "#" in trend['name']]

    # TwitterUpdateStatus
    bangkok_tz = pytz.timezone("Asia/Bangkok")
    today = datetime.datetime.now(bangkok_tz)
    tm = today.strftime("%d/%m/%Y")
    ncase = str(("🚨 ติดเชื้อใหม่ " + str(a["new_case"]) + " คน ❗\n")*3)
    ndeath = str(("⚠ เสียชีวิต " + str(a["new_death"]) + " คน\n")*3)
    timeline = str("📅 ณ วันที่ " + tm + " 📅\n \n" + ncase + ndeath + "#โควิดวันนี้ #โควิด19 " + hashtags[0] + " " + hashtags[1] + "\n \n" + "ddc.moph.go.th/covid19-dashboard")
    API.update_status(timeline)
    logging.info("Tweeted @%s", tm)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
