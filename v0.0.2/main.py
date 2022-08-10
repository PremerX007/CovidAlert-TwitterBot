import requests
import tweepy
import keys
from datetime import date

## Twitter Authentication
auth = tweepy.OAuthHandler(keys.API_KEY, keys.API_SECRET_KEY)
auth.set_access_token(keys.ACCESS_TOKEN, keys.SECRET_ACCESS_TOKEN)
print("[!] Connecting to Twiiter API >> @covidth_alert")
API = tweepy.API(auth)
print("[!] Connected!!")
print("[**] Waiting for the right time...")



url = "https://covid19.ddc.moph.go.th/api/Cases/today-cases-all"
r = requests.get(url).json()
a = r[0]

## TwitterUpdateStatus
today = date.today()
tm = today.strftime("%d/%m/%Y")
ncase = str(("🚨 ติดเชื้อใหม่ " + str(a["new_case"]) + " คน ❗\n")*4)
ndeath = str(("⚠ เสียชีวิต " + str(a["new_death"]) + " คน\n")*4)
timeline = str("📅 ณ วันที่ " + tm + " 📅\n \n" + ncase + ndeath + "#โควิดวันนี้ #โควิด19 #โควิด19วันนี้\n \n" + "ddc.moph.go.th/covid19-dashboard/")
API.update_status(timeline)



