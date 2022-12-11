import logging
from ..shared.twitter import tweet_msg
from ..shared.twitter import FecthLastestTweet
from ..shared.provincepart import *

def IndexRegionName(regions : str):
    index = {'north' : '\u0e20\u0e32\u0e04\u0e40\u0e2b\u0e19\u0e37\u0e2d', 
            'northeast' : '\u0e20\u0e32\u0e04\u0e15\u0e30\u0e27\u0e31\u0e19\u0e2d\u0e2d\u0e01\u0e40\u0e09\u0e35\u0e22\u0e07\u0e40\u0e2b\u0e19\u0e37\u0e2d',
            'central' : '\u0e20\u0e32\u0e04\u0e01\u0e25\u0e32\u0e07',
            'east' : '\u0e20\u0e32\u0e04\u0e15\u0e30\u0e27\u0e31\u0e19\u0e2d\u0e2d\u0e01',
            'south' : '\u0e20\u0e32\u0e04\u0e43\u0e15\u0e49'}
    return index[regions]

def SubReport(api,data,index_data):
    hashtags_msg = str("#โควิดวันนี้ #โควิด19")
    for region in index_data:
        index = index_data[region]
        region_name = IndexRegionName(region)
        header = str(f"🦠 จำนวนผู้ติดเชื้อใหม่ >> {region_name}")
        info = str("")
        for i in range(len(index)):
            info = info + str(f"{i+1}.{data[index[i]]['province']} {data[index[i]]['new_case']} คน\n")
            if (i+1)%7 == 0: # Split 7 choice per tweet
                if i > 7:
                    timeline = str(f"📅 สัปดาห์ที่ {data[index[i]]['weeknum']} 📅\n{header} (ต่อ)\n{info}\n{hashtags_msg}")
                    tweet_msg(msg=timeline,api=api,reply_id=FecthLastestTweet(api=api))
                else:
                    timeline = str(f"📅 สัปดาห์ที่ {data[index[i]]['weeknum']} 📅\n{header}\n{info}\n{hashtags_msg}")
                    tweet_msg(msg=timeline,api=api)
                info = str("")
                continue

            if (i+1) == (len(index)): # Tweet remain data in index
                timeline = str(f"📅 สัปดาห์ที่ {data[index[i]]['weeknum']} 📅\n{header} (ต่อ)\n{info}\n{hashtags_msg}")
                tweet_msg(msg=timeline,api=api,reply_id=FecthLastestTweet(api=api))
    
    logging.info("[ProvinceReport] ProvinceReport func complete!")

def OverallWeekReport(api,data):
    # Get Tranding Hasttag
    logging.info("[OverallDaliyReport] Get Tranding Hasttag")
    woeid = 23424960
    trends = api.get_place_trends(id = woeid)
    result_trends = trends[0]["trends"]
    hashtags = [trend['name'] for trend in result_trends if "#" in trend['name']]

    # TwitterUpdateStatus
    hashtags_msg = str(f"#โควิดวันนี้ #โควิด19 {hashtags[0]} {hashtags[1]}\n")
    daily_case = str(f"🚨 ติดเชื้อใหม่ {data['new_case']:,} คน\n")
    daily_deaths = str(f"⚠ เสียชีวิต {data['new_death']:,} คน\n")
    
    total_case = str(f"> ติดเชื้อ {data['total_case']-2223435:,} คน\n")
    total_deaths = str(f"> เสียชีวิต {data['total_death']-21698:,} คน\n")
    total_recovered = str(f"> รักษาหาย {data['total_recovered']-2168494:,} คน\n")
    timeline = str(f"📅 สัปดาห์ที่ {data['weeknum']} 📅\n\n{daily_case}{daily_deaths}\n🦠 ยอดสะสมตั้งแต่ต้นปี 🏥\n{total_case}{total_deaths}{total_recovered}{hashtags_msg}ddc.moph.go.th/covid19-dashboard")
    tweet_msg(timeline,api)
    logging.info("[OverallDaliyReport] OverallDaliyReport func complete!")

def ProvinceReport(api,data):
    index_data = province_part(data)
    SubReport(api,data,index_data)
