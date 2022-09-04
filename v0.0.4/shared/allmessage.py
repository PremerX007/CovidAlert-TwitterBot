import logging
from ..shared.twitter import tweet_msg
from ..shared.twitter import FecthLastestTweet

def IndexProvince(regions : str):
    index = {'north' : [70,71,46,47,76,31,23,75,67,14], 
    'northeast' : [65,24,25,10,3,5,74,37,38,17,18,63,62,41,49,48,60,69,66,40],
    'central' : [1,30,26,21,16,52,64,9,45,53,54,55,57,58,15,2,27,44,72,61,34,35,4,73,20,68],
    'east' : [6,7,8,13,28,43,56],
    'south' : [0,11,12,19,22,29,32,33,36,39,42,50,51,59]} 
    return index[regions]

def IndexRegionName(regions : str):
    index = {'north' : 'ภาคเหนือ', 
    'northeast' : 'ภาคตะวันออกเฉียงเหนือ',
    'central' : 'ภาคกลาง',
    'east' : 'ภาคตะวันออก',
    'south' : 'ภาคใต้'} 
    return index[regions]

def SubReportOverchar(regions : str,api,data,time):
    try:
        index_af = IndexProvince(regions)
        index_be = [index_af.pop(0) for i in range(int(len(index_af)/2))]
        region_name = IndexRegionName(regions)
        hashtags_msg = str("#โควิดวันนี้ #โควิด19")
        header = str(f'🦠 จำนวนผู้ติดเชื้อใหม่ *{region_name}*\n')
        info = str('')
        for i in range(len(index_be)):
            info = info + str(f'{i+1}.{data[index_be[i]]["province"]} {data[index_be[i]]["new_case"]} คน\n')
        show_date = time.strftime("%d/%m/%Y")
        timeline = str(f"📅 ณ วันที่ {show_date} 📅\n{header}{info}\n{hashtags_msg}")
        tweet_msg(timeline,api)
        info = str('')
        for i in range(len(index_af)):
            info = info + str(f'{i+len(index_af)+1}.{data[index_af[i]]["province"]} {data[index_af[i]]["new_case"]} คน\n')
        timeline = str(f"📅 ณ วันที่ {show_date} 📅\n{header}(*ต่อ)\n{info}\n{hashtags_msg}")
        tweet_msg(timeline,api,reply_id=FecthLastestTweet(api))
    except:
        index_af = IndexProvince(regions)
        index_be = [index_af.pop(0) for i in range(int(len(index_af)/2))]
        region_name = IndexRegionName(regions)
        hashtags_msg = str("#โควิดวันนี้")
        header = str(f'🦠 ติดเชื้อใหม่วันนี้ >{region_name}\n')
        info = str('')
        for i in range(len(index_be)):
            info = info + str(f'{i+1}.{data[index_be[i]]["province"]} {data[index_be[i]]["new_case"]} คน\n')
        timeline = str(f"{header}{info}{hashtags_msg}")
        tweet_msg(timeline,api)
        info = str('')
        for i in range(len(index_af)):
            info = info + str(f'{i+len(index_af)+1}.{data[index_af[i]]["province"]} {data[index_af[i]]["new_case"]} คน\n')
        timeline = str(f"{header}{info}{hashtags_msg}")
        tweet_msg(timeline,api,reply_id=FecthLastestTweet(api))

def SubReport(regions : str,api,data,time):
    index = IndexProvince(regions)
    region_name = IndexRegionName(regions)
    hashtags_msg = str("#โควิดวันนี้ #โควิด19")
    header = str(f'🦠 จำนวนผู้ติดเชื้อใหม่ *{region_name}*\n')
    info = str('')
    for i in range(len(index)):
        info = info + str(f'{i+1}.{data[index[i]]["province"]} {data[index[i]]["new_case"]} คน\n')
    show_date = time.strftime("%d/%m/%Y")
    timeline = str(f"📅 ณ วันที่ {show_date} 📅\n{header}{info}\n{hashtags_msg}")
    tweet_msg(timeline,api)

def OverallDaliyReport(api,data,time):
    # Get Tranding Hasttag
    logging.info("[OverallDaliyReport] Get Tranding Hasttag")
    woeid = 23424960
    trends = api.get_place_trends(id = woeid)
    result_trends = trends[0]["trends"]
    hashtags = [trend['name'] for trend in result_trends if "#" in trend['name']]

    # TwitterUpdateStatus
    show_date = time.strftime("%d/%m/%Y")
    daily_case = str(f"🚨 ติดเชื้อใหม่ {data['new_case']} คน\n")
    daily_deaths = str(f"⚠ เสียชีวิต {data['new_death']} คน\n")
    daily_recovered = str(f"💚 รักษาหายแล้ว {data['new_recovered']} คน\n")
    hashtags_msg = str(f"#โควิดวันนี้ #โควิด19 {hashtags[0]} {hashtags[1]}\n\n")
    timeline = str(f"📅 ณ วันที่ {show_date} 📅\n\n{daily_case}{daily_deaths}{daily_recovered}{hashtags_msg}ddc.moph.go.th/covid19-dashboard")
    tweet_msg(timeline,api)
    logging.info("[OverallDaliyReport] OverallDaliyReport func complete!")

def ProvinceReport(api,data,time):
    SubReport('north',api,data,time)
    SubReportOverchar('northeast',api,data,time)
    SubReportOverchar('central',api,data,time)
    SubReport('east',api,data,time)
    SubReportOverchar('south',api,data,time)
    logging.info("[ProvinceReport] ProvinceReport func complete!")

# if __name__ == '__main__':
#     SubReportOverchar('central',data=requests.get("https://covid19.ddc.moph.go.th/api/Cases/today-cases-by-provinces").json()) #Test Panels