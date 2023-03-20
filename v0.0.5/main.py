import requests
import pytz
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
from subconfig.twitter import APIAuth, FecthLastestTweet
from subconfig.allmessage import OverallWeekReport, ProvinceReport

# URLs API MOPH
overall_url = "https://covid19.ddc.moph.go.th/api/Cases/today-cases-all"
province_url = "https://covid19.ddc.moph.go.th/api/Cases/today-cases-by-provinces"
vaccine_url = "https://covid19.ddc.moph.go.th/api/Vaccinated/weekly-vaccinated"
pv_vaccine_url = "https://covid19.ddc.moph.go.th/api/Vaccinated/weekly-vaccinated-by-provice"

def AuthDataChecker():
    try:
        datatest = requests.get(overall_url).json()[0]
        datatest2 = requests.get(vaccine_url).json()[0]
        print("✅[PROCESS] AuthDataChecker")
        return True
    except KeyError:
        # Error Ring-Balancer
        print("🚨[ERROR] Ring-Balancer")
        return False
    except IndexError:
        # Error Data in json is empty
        try:
            datatest = requests.get(overall_url).json()[0]
        except IndexError:
            print("🚨[ERROR] Data in overall json is empty")
            return False
        
        try:
            datatest2 = requests.get(vaccine_url).json()[0]
        except IndexError:
            print("⚠ [WARNING] Data in vaccine json is empty")
            return True            
    except requests.exceptions.ConnectionError:
        print("🚨[ERROR] Can not connect to api")
        # Error Connection pool
        return False

def main():
    # Setting Time&Date
    bangkok_tz = pytz.timezone("Asia/Bangkok")
    th_time = datetime.now(bangkok_tz)

    # Twiiter
    api = APIAuth()
    date_tweeted_fecth = FecthLastestTweet(api,week=True)
    
    # Get Data From MOPH API
    data = requests.get(overall_url).json()[0]
    data_province = requests.get(province_url).json()

    try:
        data_vaccine = requests.get(vaccine_url).json()[0]
        data_vac_pv = requests.get(pv_vaccine_url).json()
    except IndexError:
        data_vaccine = None
        data_vac_pv = None

    print("[REQUESTS] Data received.")

    
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
    if (AuthDataChecker()): 
        main()