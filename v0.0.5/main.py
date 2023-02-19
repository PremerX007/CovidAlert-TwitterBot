import requests
import pytz
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
from subconfig.twitter import APIAuth, FecthLastestTweet
from subconfig.allmessage import OverallWeekReport, ProvinceReport

def main():
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
    try: # Check The APIs is accessible or not.
        try:
            data = requests.get(overall_url).json()[0]
            data_province = requests.get(province_url).json()
            data_vaccine = requests.get(vaccine_url).json()[0]
            data_vac_pv = requests.get(pv_vaccine_url).json()
            print("[REQUESTS] Data received.")
        except KeyError:
            data = requests.get(overall_url).json()
            print("[REQUESTS] not the required information.")
            print(f"🚨[ERROR] Pls Check APIs -> {str(data)}")
            raise ValueError("Noob Admin please check this again!!")
        except Exception:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
            data = requests.get(overall_url, verify=False).json()[0]
            data_province = requests.get(province_url, verify=False).json()
            data_vaccine = requests.get(vaccine_url, verify=False).json()[0]
            data_vac_pv = requests.get(pv_vaccine_url, verify=False).json()
            print("[REQUESTS] Data (not verify SSL) received")
            if data['weeknum'] != date_tweeted_fecth:
                print("🚩[WARNING] Unverified HTTPS request to host 'covid19.ddc.moph.go.th' [SSLCert not verify]")
    except Exception as exc:
        print(f"[REQUESTS] 🚨 Unable to connect DDC MOPH APIs | Error >> {type(exc)} {exc}")
        raise ValueError("Noob Admin please check this again!!")
    else:
        # Work process
        if data['weeknum'] != date_tweeted_fecth:
            # Report per province
            ProvinceReport(api=api, data=data_province, data_vac=data_vac_pv)
            # Report Overall
            OverallWeekReport(api=api, data=data, data_vac=data_vaccine)
            info_datetime = th_time.strftime("%d-%m-%y" + '@' + "%H:%M")
            # Status
            print(f"✅[INFO] Tweeted !! at {info_datetime}")
        # Monitor idle
        else:
            print("[IDLE] Data has already tweeted.")

if __name__ == '__main__':
    main()
    