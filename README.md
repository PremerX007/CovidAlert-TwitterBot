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
    <img src ="https://user-images.githubusercontent.com/39229888/183920557-1f2f21b4-a173-4961-977b-ed99775566c0.png" />
  </a>
</div>

## :floppy_disk: Versions
### - [0.0.1 (Outdated)](v0.0.1/)
This version used this [``requirements``](v0.0.1/requirements.txt)
```
opencv-python
pytesseract
tweepy
selenium
```
เวอร์ชันนี้ถือว่าลากเลือดที่สุด โดยเป็นการให้ตัวโปรแกรม [``scrshot.py``](v0.0.1/scrshot.py) ไปรับรูปภาพเป็นข้อมูลตัวเลขจาก [กรมควบคุมโรค](https://covid19.ddc.moph.go.th/)โดยใช้ Selenium ในการทำงาน จะได้รูปภาพนี้มา

<img src ="https://user-images.githubusercontent.com/39229888/184527459-85e1ce93-666e-4f2f-ac9a-75ff4ae8abcf.png" />

จากนั้นนำภาพมาทำภาพขาวดำและครอปภาพโดยใช้ [**OpenCV**](https://opencv.org/) เพื่อส่งต่อข้อมูลไปให้ [**Pytesseract**](https://github.com/tesseract-ocr/tesseract) ประมวลผลเป็นตัวเลข เก็บไว้ในตัวแปรเพื่อทำการ Tweet ต่อไปโดยที่โปรแกรมถูกตั้งเวลาการทำงานไว้ที่เวลา 8 โมงเช้าของทุกวัน

<img src ="https://user-images.githubusercontent.com/39229888/184527468-95c0cb89-98c8-4dc1-9f6e-15a64dbdaa97.png" />

**P.S. ในขณะนั้น API ของตัวเลขผู้ติดเชื้อและผู้เสียชีวิตจากโควิด-19 ของกรมควบคุมโรคยังไม่เสถียรและมีความช้าในด้านการอัพเดทข้อมูลแต่ละวันเป็นอย่างมาก เลยเลี่ยงที่จะใช้งาน**

### - [0.0.2](v0.0.2/)
This version used this [``requirements``](v0.0.2/requirements.txt)
```
requests
tweepy
```
เวอร์ชันได้อัพเดทจาก v0.0.1 เป็นอย่างมาก หลังจากที่ API ของกรมควมคุมโรค มีความเสถียร (มีการอัพเดทข้อมูลในตอนเช้า ประมาณ 7:30 โดยประมาณ) ทำให้ง่ายต่อการรับข้อมูลมา ทำให้ตัวโปรแกรมทำงานแค่ดึง JSON มาอ่านและทำการ Tweet แค่นั้นเอง

```python
## Request JSON
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
```
### - [0.0.3](v0.0.3/)

## :pray: Bigthank for API Covid Data
- [Department of Disease Control](https://covid19.ddc.moph.go.th/)
