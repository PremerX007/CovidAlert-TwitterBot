import pytesseract
import tweepy
import crop
import keys
import time
from scrshot import collect_data
from crop import croppic
from datetime import date

## Twitter Authentication
auth = tweepy.OAuthHandler(keys.API_KEY, keys.API_SECRET_KEY)
auth.set_access_token(keys.ACCESS_TOKEN, keys.SECRET_ACCESS_TOKEN)
print("[!] Connecting to Twiiter API >> @covidth_alert")
API = tweepy.API(auth)
print("[!] Connected!!")
print("[**] Waiting for the right time...")

while(True):
    named_tuple = time.localtime()
    time_string = time.strftime("%H:%M:%S", named_tuple)
    status_time = time.strftime("%d/%m/%Y || %H:%M:%S", named_tuple)
    while (time_string == "08:00:00"):
        print("********************************************")
        print("   Script Start At " + status_time)
        print("********************************************")
        collect_data()

        ## Process DATA
        data = croppic()
        newinfect = data[crop.y:crop.y+crop.h, crop.x:crop.x+crop.w]
        newdeath = data[crop.y1:crop.y1+crop.h1, crop.x1:crop.x1+crop.w1]

        ## Tesseract OCR
        print("[!] Process Data By TESSERACT ORC")
        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        new = list(pytesseract.image_to_string(newinfect))
        die = list(pytesseract.image_to_string(newdeath))

        ## TwitterUpdateStatus
        today = date.today()
        tm = today.strftime("%d/%m/%Y")
        timeline = str("📅 วันที่ " + tm + " 📅\n \n" + "🚨🚨🚨 ยอดติดเชื้อเพิ่มวันนี้ : " + ''.join(new[:-2]) + " คน ❗❗\n" + "⚠⚠ เสียชีวิต : " + ''.join(die[:-2]) + " คน\n" + "#โควิดวันนี้ #โควิด19 #โควิด19วันนี้\n \n" + "ddc.moph.go.th/covid19-dashboard/")
        API.update_status(timeline)
        print("[!] Tweeted !!")
        print("\n[**] Waiting for the right time...")
        break

        ## TEST CONSOLE
        # print(timeline)
        # cv2.imshow('Result',newinfect)
        # cv2.imshow('Result2',newdeath)
        # cv2.waitKey(0)
