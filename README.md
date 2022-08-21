# Covid Alert TwitterBot
[![Twitter](https://img.shields.io/twitter/url?label=Twitter&style=social&url=https%3A%2F%2Ftwitter.com%2Fcovidth_alert)](https://twitter.com/covidth_alert)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/PremerX007/Covid_Alert_TwitterBot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/PremerX007/Covid_Alert_TwitterBot/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/PremerX007/Covid_Alert_TwitterBot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/PremerX007/Covid_Alert_TwitterBot/context:python)

### :loudspeaker: **บอทกำลังอยู่ในช่วงการทดสอบ** :hammer_and_wrench: บน Microsoft Azure Function **(Serverless)** :toolbox:

# :wave: About
ตัวบอทสร้างมาเพื่อวัตถุประสงค์ในการแจ้งจำนวนผู้ติดเชื้อและผู้เสียชีวิตจากไวรัส SARS-CoV-2 ของประเทศไทยในแต่ละวัน 

- [Twitter of @covidth_alert](https://twitter.com/covidth_alert)

<div style="text-align:center">
  <a href="https://twitter.com/covidth_alert">
    <img src ="https://user-images.githubusercontent.com/39229888/184621341-e6002c1f-a089-4ec5-ad1c-f8dda54298c1.jpg" />
  </a>
</div>

## :floppy_disk: Versions
### - [v0.0.1 (Outdated)](v0.0.1/)
This version used this [``requirements``](v0.0.1/requirements.txt)
```
opencv-python
pytesseract
tweepy
selenium
```
เวอร์ชันนี้เป็นเวอร์ชันทำเรื่องง่ายให้เป็นเรื่องยาก โดยเป็นการให้ตัวโปรแกรม [``scrshot.py``](v0.0.1/scrshot.py) ไป Download รูปภาพข้อมูลตัวเลขจาก [กรมควบคุมโรค](https://ddc.moph.go.th/covid19-dashboard/)โดยใช้ Selenium ในการทำงาน จะได้รูปภาพนี้มา

<img src ="https://user-images.githubusercontent.com/39229888/184527459-85e1ce93-666e-4f2f-ac9a-75ff4ae8abcf.png" />

จากนั้นนำภาพมาทำภาพขาวดำและครอปภาพโดยใช้ [**OpenCV**](https://opencv.org/) เพื่อส่งต่อข้อมูลไปให้ [**Pytesseract OCR**](https://github.com/tesseract-ocr/tesseract) ประมวลผลเป็นตัวเลข เก็บไว้ในตัวแปรเพื่อทำการ Tweet ต่อไปโดยที่โปรแกรมถูกตั้งเวลาการทำงานไว้ที่เวลา 8 โมงเช้าของทุกวัน

<img src ="https://user-images.githubusercontent.com/39229888/184527468-95c0cb89-98c8-4dc1-9f6e-15a64dbdaa97.png" />

**P.S. ในขณะนั้น API ของตัวเลขผู้ติดเชื้อและผู้เสียชีวิตจากโควิด-19 ของกรมควบคุมโรคยังไม่เสถียรและมีความช้าในด้านการอัพเดทข้อมูลแต่ละวันเป็นอย่างมาก เลยเลี่ยงที่จะใช้งาน**

**:exclamation: This version may not work in other environments if you don't config. (e.g. selenium, pytesseract)**

### - [v0.0.2](v0.0.2/)
This version used this [``requirements``](v0.0.2/requirements.txt)
```
requests
tweepy
```
เวอร์ชันได้อัพเดทจาก [v0.0.1](v0.0.1/) เป็นอย่างมาก (ชึ่งแตกต่างจากเวอร์ชันเดิมที่ต้องใช้ libary เป็นจำนวนมาก) หลังจากที่ API ของ[กรมควมคุมโรค](https://covid19.ddc.moph.go.th/)มีความเสถียร (มีการอัพเดทข้อมูลในตอนเช้า ประมาณ 7:30 โดยประมาณ) ทำให้ง่ายต่อการรับข้อมูลมา **ทำให้ตัวโปรแกรมทำงานแค่ดึง JSON มาอ่านและทำการ Tweet** แค่นั้นเอง

```python
# Request JSON
url = "https://covid19.ddc.moph.go.th/api/Cases/today-cases-all"
data_all = requests.get(url).json()[0]

# TwitterUpdateStatus
show_date = th_time.strftime("%d/%m/%Y")
daily_case = str(("🚨 ติดเชื้อใหม่ " + str(data_all["new_case"]) + " คน ❗\n")*3)
daily_deaths = str(("⚠ เสียชีวิต " + str(data_all["new_death"]) + " คน\n")*3)
timeline = str("📅 ณ วันที่ " + show_date + " 📅\n \n" + daily_case + daily_deaths + "#โควิดวันนี้ #โควิด19 " + hashtags[0] + " " + hashtags[1] + "\n \n" + "ddc.moph.go.th/covid19-dashboard")
API.update_status(timeline)
logging.info("Twitter update status @%s", show_date)
```
### - [v0.0.3](v0.0.3/)
เวอร์ชันนี้ใช้ตัวโปรแกรมจากเวอร์ชัน [v0.0.2](v0.0.2/) แต่นำไปรันบน Serverless ของ Azure ทำการ Config อะไรเล็กๆน้อยๆ
* มีการเพิ่ม LINE Notify แจ้งเตือนเมื่อโปรแกรมเริ่มทำงาน เพื่อเช็คการทำงานของโปรแกรมว่าทำงานได้ปกติดี
```python
# line notify
line_url = 'https://notify-api.line.me/api/notify'
HEADERS = {'Authorization': 'Bearer ' + api.LINE_TOKEN}
line_info_timenow = th_time.strftime("%d-%m-%Y" + '@' + "%H:%M")
msg = line_info_timenow + " [INFO] Script Working!! : Microsoft Azure Serverless" 
response = requests.post(line_url,headers=HEADERS,params={"message": msg})
logging.info(response)
logging.info("LINE Notify : %s", response)
```
<img width="541" alt="ภาพประเภท PNG 2022-08-14 11_01_32" src="https://user-images.githubusercontent.com/39229888/184533766-82fe303f-afed-4e9b-9090-942ff80233fa.png">

* เพิ่มการหา Trending Hashtags ของประเทศไทย
```python
# Get Tranding Hashtag in TH
woeid = 23424960 # number of WOEID (Where On Earth IDentifier) of Thailand
trends = API.get_place_trends(id = woeid)
result_trends = trends[0]["trends"]
hashtags = [trend['name'] for trend in result_trends if "#" in trend['name']]
```
* เพิ่ม logic ตรวจสอบว่าข้อมูลวันนี้ทวีตไปแล้วหรือยัง ถ้ายังให้ทำการทวีต แต่ถ้าทวีตไปแล้วจะไม่ทำการทวีตอีก

:grey_question::tired_face: บางวัน API มีการอัพเดทที่ล่าช้า เมื่อ**ตั้ง Timer ไว้อย่างเดียวแล้วไม่มีการเช็ค ตัวโปรแกรมอาจจะนำข้อมูลของวันก่อนหน้ามาทวีตได้**
```python
# Fecth Tweeted Timeline
logging.info("[!] Fecthing Tweeted Timeline")
data_tweets = API.user_timeline(user_id=api.TWITTER_ID, count=1)
for tweet in data_tweets:
  date_tweeted_fecth = str(tweet.created_at)[:-15]

if data_all['txn_date'] == date_now and date_tweeted_fecth != date_now:
  ### Work Process
elif date_tweeted_fecth != date_now:
  logging.info("Wait for new data from API.")
else:
  logging.info("Today has already tweeted data.")
```

## :pray: Bigthank for API Covid Data
- [Department of Disease Control](https://covid19.ddc.moph.go.th/)
