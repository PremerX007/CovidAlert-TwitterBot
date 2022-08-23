# Covid Alert TwitterBot
[![Twitter](https://img.shields.io/twitter/url?label=Twitter&style=social&url=https%3A%2F%2Ftwitter.com%2Fcovidth_alert)](https://twitter.com/covidth_alert)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/PremerX007/Covid_Alert_TwitterBot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/PremerX007/Covid_Alert_TwitterBot/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/PremerX007/Covid_Alert_TwitterBot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/PremerX007/Covid_Alert_TwitterBot/context:python)

### :loudspeaker: **In the process of testing the system** :hammer_and_wrench: on Microsoft Azure :toolbox:

# :wave: About
Twitter bot for daily reporting of SARS-CoV-2 cases and deaths in Thailand.

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
The process in this version uses this script [``scrshot.py``](v0.0.1/scrshot.py) to download data images from [Department of Disease Control](https://ddc.moph.go.th/covid19-dashboard/) website by using Selenium to work, you will get this image.

<img src ="https://user-images.githubusercontent.com/39229888/184527459-85e1ce93-666e-4f2f-ac9a-75ff4ae8abcf.png" />

Then import the image to make a black and white image, crop it using [**OpenCV**](https://opencv.org/), and forward the processed image to [**Pytesseract OCR**](https://github.com/tesseract-ocr/tesseract) converted to numbers Store it in a variable to continue Tweeting, with the program set to run at 8 a.m. every day.

<img src ="https://user-images.githubusercontent.com/39229888/184527468-95c0cb89-98c8-4dc1-9f6e-15a64dbdaa97.png" />

**P.S. At that time, the API of the number of cases and deaths from COVID-19 from the Department of Disease Control is not stable and is very slow in updating information each day. As a result, avoid using**

**:exclamation: This version may not work in other environments if you don't config. (e.g. selenium, pytesseract)**

### - [v0.0.2](v0.0.2/)
This version used this [``requirements``](v0.0.2/requirements.txt)
```
requests
tweepy
```
This version has greatly improved upon the previous version . (This is different from [v0.0.1](v0.0.1/) version that required a lot of libraries). After the [Department of Disease Control APIs](https://covid19.ddc.moph.go.th/) stabilized (data was updated around 7:30 a.m.), it became easier to obtain information. accurate and on time. 

**Make the script work by simply extracting numbers from the API in the form of JSON data format to read and tweet.**

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
This version uses the program from the [previous version (v0.0.2)](v0.0.2/). However, bring it to run on the Microsoft Azure cloud and adapt some of the scripts to the environment required by the cloud. and developed this version until now, with various sub-feature updates such as

* LINE Notify has been added to notify you when the program starts. to check whether the program works properly or not.
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
<img src="https://user-images.githubusercontent.com/39229888/186081650-1f51678c-9e98-4f0e-ac52-c36f7b977e91.jpg"/>

* Add Thailand Trending Hashtags to increase the visibility of tweets.
```python
# Get Tranding Hashtag in TH
woeid = 23424960 # number of WOEID (Where On Earth IDentifier) of Thailand
trends = API.get_place_trends(id = woeid)
result_trends = trends[0]["trends"]
hashtags = [trend['name'] for trend in result_trends if "#" in trend['name']]
```
* I added checking if today's information has been tweeted or not. If not, make a tweet. But if I have already tweeted, I will not tweet again to prevent retweeting the same information.
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
:grey_question::tired_face: Recently, the API came back to update information late. Therefore, **the method of scheduling tweets at 8 a.m. was removed to prevent tweeting from the previous day's data.** and conditionally check the time directly with the API to get the data according to the correct date and time.

## :pray: Bigthank for DDC API Covid Data TH
- [Department of Disease Control](https://covid19.ddc.moph.go.th/)
