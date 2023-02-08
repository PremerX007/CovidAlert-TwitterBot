import logging
import requests
import pytz
import azure.functions as func
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
from ..shared.twitter import APIAuth, FecthLastestTweet
from ..shared.allmessage import OverallWeekReport, ProvinceReport
from ..shared.linenoti import line_notify

def main(covidth : func.TimerRequest):
    if covidth.past_due:
        logging.info('System is past due!')

    # Setting Time&Date
    bangkok_tz = pytz.timezone("Asia/Bangkok")
    th_time = datetime.now(bangkok_tz)

    # Twiiter
    api = APIAuth()
    date_tweeted_fecth = FecthLastestTweet(api,week=True)
    
    # Get Data From MOPH API
    overall_url = "https://covid19.ddc.moph.go.th/api/Cases/today-cases-all"
    province_url = "https://covid19.ddc.moph.go.th/api/Cases/today-cases-by-provinces"
    vaccine_url = "https://covid19.ddc.moph.go.th/api/Vaccinated/weekly-vaccinated"
    pv_vaccine_url = "https://covid19.ddc.moph.go.th/api/Vaccinated/weekly-vaccinated-by-provice"

    try: # Check The APIs is accessible or not to get.
        try:
            data = requests.get(overall_url).json()[0]
            data_province = requests.get(province_url).json()
            data_vaccine = requests.get(vaccine_url).json()[0]
            data_vac_pv = requests.get(pv_vaccine_url).json()
            logging.info("[REQUESTS] Data received.")

        except KeyError:
            data = requests.get(overall_url).json()
            logging.info("[REQUESTS] not the required information.")
            line_notify(f"🚨[ERROR] Pls Check APIs -> {str(data)}", stickerPackageId=11539, stickerId=52114142)

        except Exception:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
            data = requests.get(overall_url, verify=False).json()[0]
            data_province = requests.get(province_url, verify=False).json()
            data_vaccine = requests.get(vaccine_url, verify=False).json()[0]
            data_vac_pv = requests.get(pv_vaccine_url, verify=False).json()
            logging.warning("[REQUESTS] Data (not verify SSL) received")

            if data['weeknum'] != date_tweeted_fecth:
                line_notify("🚩[WARNING] Unverified HTTPS request to host 'covid19.ddc.moph.go.th' [SSLCert not verify]", stickerPackageId=789, stickerId=10877)

    except Exception as exc:
        logging.error(f"[REQUESTS] Unable to connect DDC MOPH APIs | Error >> {type(exc)} {exc}")
        line_notify("🚨[ALERT] Unable to connect DDC MOPH APIs")
        line_notify(f"🚨[ERROR] {type(exc)} {exc}", stickerPackageId=11539, stickerId=52114142)

    else:
        # Work process
        if data['weeknum'] != date_tweeted_fecth:
            # Report per province
            ProvinceReport(api=api, data=data_province, data_vac=data_vac_pv)
            # Report Overall
            OverallWeekReport(api=api, data=data, data_vac=data_vaccine)
            # Line Notificaions
            line_info_datetime = th_time.strftime("%d-%m-%y" + '@' + "%H:%M")
            line_notify(f"✅[INFO] Tweeted !! at {line_info_datetime}", stickerPackageId=11539, stickerId=52114117)

        # Monitor idle
        else:
            logging.info("[IDLE] Data has already tweeted.")