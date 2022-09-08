import logging
from ..shared.twitter import tweet_msg
from ..shared.twitter import FecthLastestTweet

index_data = {'north' : [70,71,46,47,76,31,23,75,67,14], 
    'northeast' : [65,24,25,10,3,5,74,37,38,17,18,63,62,41,49,48,60,69,66,40],
    'central' : [1,30,26,21,16,52,64,9,45,53,54,55,57,58,15,2,27,44,72,61,34,35,4,73,20,68],
    'east' : [6,7,8,13,28,43,56],
    'south' : [0,11,12,19,22,29,32,33,36,39,42,50,51,59]} 

def IndexRegionName(regions : str):
    index = {'north' : '\u0e20\u0e32\u0e04\u0e40\u0e2b\u0e19\u0e37\u0e2d', 
    'northeast' : '\u0e20\u0e32\u0e04\u0e15\u0e30\u0e27\u0e31\u0e19\u0e2d\u0e2d\u0e01\u0e40\u0e09\u0e35\u0e22\u0e07\u0e40\u0e2b\u0e19\u0e37\u0e2d',
    'central' : '\u0e20\u0e32\u0e04\u0e01\u0e25\u0e32\u0e07',
    'east' : '\u0e20\u0e32\u0e04\u0e15\u0e30\u0e27\u0e31\u0e19\u0e2d\u0e2d\u0e01',
    'south' : '\u0e20\u0e32\u0e04\u0e43\u0e15\u0e49'}
    return index[regions]

def SortIndex(data):
    def sort(k):
        return data[k]['new_case']

    for i in index_data:
        index_data[i].sort(reverse=True,key=sort)

def SubReport(api,data,time):
    hashtags_msg = str("#โควิดวันนี้ #โควิด19")
    for region in index_data:
        index = index_data[region]
        region_name = IndexRegionName(region)
        header = str(f"🦠 จำนวนผู้ติดเชื้อใหม่ >> {region_name}")
        info = str("")
        show_date = time.strftime("%d/%m/%Y")
        for i in range(len(index)):
            info = info + str(f"{i+1}.{data[index[i]]['province']} {data[index[i]]['new_case']} คน\n")
            if (i+1)%7 == 0: # Split 7 choice per tweet
                if i > 7:
                    timeline = str(f"📅 ณ วันที่ {show_date} 📅\n{header} (ต่อ)\n{info}\n{hashtags_msg}")
                    tweet_msg(msg=timeline,api=api,reply_id=FecthLastestTweet(api=api))
                else:
                    timeline = str(f"📅 ณ วันที่ {show_date} 📅\n{header}\n{info}\n{hashtags_msg}")
                    tweet_msg(msg=timeline,api=api)
                info = str("")
                continue

            if (i+1) == (len(index)): # Tweet remain data in index
                timeline = str(f"📅 ณ วันที่ {show_date} 📅\n{header} (ต่อ)\n{info}\n{hashtags_msg}")
                tweet_msg(msg=timeline,api=api,reply_id=FecthLastestTweet(api=api))

def OverallDaliyReport(api,data,data_total,time):
    # Get Tranding Hasttag
    logging.info("[OverallDaliyReport] Get Tranding Hasttag")
    woeid = 23424960
    trends = api.get_place_trends(id = woeid)
    result_trends = trends[0]["trends"]
    hashtags = [trend['name'] for trend in result_trends if "#" in trend['name']]

    # TwitterUpdateStatus
    show_date = time.strftime("%d/%m/%Y")
    hashtags_msg = str(f"#โควิดวันนี้ #โควิด19 {hashtags[0]} {hashtags[1]}\n")
    daily_case = str(f"🚨 ติดเชื้อใหม่ {data['new_case']} คน\n")
    daily_deaths = str(f"⚠ เสียชีวิต {data['new_death']} คน\n")
    daily_recovered = str(f"💚 รักษาหายแล้ว {data['new_recovered']} คน\n")
    
    total_case = str(f"> ติดเชื้อ {data_total['total_case']-2223435} คน\n")
    total_deaths = str(f"> เสียชีวิต {data_total['total_death']-21698} คน\n")
    total_recovered = str(f"> รักษาหาย {data_total['total_recovered']-2168494} คน\n")
    timeline = str(f"📅 ณ วันที่ {show_date} 📅\n\n{daily_case}{daily_deaths}{daily_recovered}\n🦠 ยอดสะสมตั้งแต่ต้นปี 🏥\n{total_case}{total_deaths}{total_recovered}{hashtags_msg}ddc.moph.go.th/covid19-dashboard")
    tweet_msg(timeline,api)
    logging.info("[OverallDaliyReport] OverallDaliyReport func complete!")

def ProvinceReport(api,data,time):
    SortIndex(data)
    SubReport(api,data,time)
    logging.info("[ProvinceReport] ProvinceReport func complete!")

# if __name__ == '__main__':
#     SubReportOverchar('central',data=requests.get("https://covid19.ddc.moph.go.th/api/Cases/today-cases-by-provinces").json()) #Test Panels