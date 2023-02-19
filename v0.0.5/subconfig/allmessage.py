from subconfig.twitter import FecthLastestTweet, Tweet_msg
from subconfig.provincepart import Province_part

def IndexRegionName(regions : str):
    index = {'north' : '\u0e20\u0e32\u0e04\u0e40\u0e2b\u0e19\u0e37\u0e2d', 
            'northeast' : '\u0e20\u0e32\u0e04\u0e15\u0e30\u0e27\u0e31\u0e19\u0e2d\u0e2d\u0e01\u0e40\u0e09\u0e35\u0e22\u0e07\u0e40\u0e2b\u0e19\u0e37\u0e2d',
            'central' : '\u0e20\u0e32\u0e04\u0e01\u0e25\u0e32\u0e07',
            'east' : '\u0e20\u0e32\u0e04\u0e15\u0e30\u0e27\u0e31\u0e19\u0e2d\u0e2d\u0e01',
            'south' : '\u0e20\u0e32\u0e04\u0e43\u0e15\u0e49'}
    return index[regions]

def SubReport(api, data, index_data):
    hashtags_msg = str("#โควิดวันนี้ #โควิด19")
    for region in index_data:
        if region == "allzone": break
        index = index_data[region]
        region_name = IndexRegionName(region)
        header = str(f"🦠 จำนวนผู้ติดเชื้อใหม่ >> {region_name}")
        info = str("")
        for i in range(len(index)):
            info = info + str(f"{i+1}.{data[index[i]]['province']} {data[index[i]]['new_case']} คน\n")
            if (i+1)%7 == 0: # Split 7 choice per tweet
                if i > 7:
                    timeline = str(f"📅 สัปดาห์ที่ {data[index[i]]['weeknum']} 📅\n{header} (ต่อ)\n{info}\n{hashtags_msg}")
                    Tweet_msg(msg=timeline,api=api,reply_id=FecthLastestTweet(api=api))
                else:
                    timeline = str(f"📅 สัปดาห์ที่ {data[index[i]]['weeknum']} 📅\n{header}\n{info}\n{hashtags_msg}")
                    Tweet_msg(msg=timeline,api=api)
                info = str("")
                continue

            if (i+1) == (len(index)): # Tweet remain data in index
                if i+1 > 7:
                    tor = str("(ต่อ)")
                    reply_flag = FecthLastestTweet(api=api)
                else:
                    tor = str("")
                    reply_flag = None
                    
                timeline = str(f"📅 สัปดาห์ที่ {data[0]['weeknum']} 📅\n{header} {tor}\n{info}\n{hashtags_msg}")
                Tweet_msg(msg=timeline,api=api,reply_id=reply_flag)
    
    print("[ProvinceReport] ProvinceReport func complete!")

def OverallWeekReport(api, data, data_vac):
    # Get Tranding Hasttag
    print("[OverallDaliyReport] Get Tranding Hasttag")
    woeid = 23424960
    trends = api.get_place_trends(id = woeid)
    result_trends = trends[0]["trends"]
    hashtags = [trend['name'] for trend in result_trends if "#" in trend['name']]

    # TwitterUpdateStatus
    hashtags_msg = str(f"#โควิดวันนี้ #โควิด19 {hashtags[0]} {hashtags[1]}\n")
    daily_case = str(f"🚨 ติดเชื้อใหม่ {data['new_case']:,} คน\n")
    daily_deaths = str(f"⚠ เสียชีวิต {data['new_death']:,} คน\n")
    daily_vaccine = str(f"💉 รับวัคซีนแล้ว {data_vac['vaccine_total']:,} โดส\n")
    
    total_case = str(f"> ติดเชื้อ {data['total_case']:,} คน\n")
    total_deaths = str(f"> เสียชีวิต {data['total_death']:,} คน\n\n")
    timeline = str(f"📅 สัปดาห์ที่ {data['weeknum']} 📅\n\n{daily_case}{daily_deaths}{daily_vaccine}\n🦠 ยอดสะสมตั้งแต่ต้นปี 🏥\n{total_case}{total_deaths}{hashtags_msg}ddc.moph.go.th/covid19-dashboard")
    Tweet_msg(timeline,api)
    print("[OverallDaliyReport] OverallDaliyReport func complete!")

def VaccineRankingReport(api, data_vac, index_data):
    header = (f"💉 จำนวนวัคซีนของแต่ละจังหวัดที่ประชาชนได้รับ\n👨‍⚕️ สัปดาห์ที่ {data_vac[0]['weeknum']} ของปี 2023 🇹🇭\n")
    info = str("")
    rank = 1
    for data in index_data['allzone']:
        info += (f"{rank}.{data_vac[data]['province']} {data_vac[data]['vaccine_total']:,} โดส\n")
        if rank%7 == 0:
            if rank > 7:
                Tweet_msg(msg=info,api=api,reply_id=FecthLastestTweet(api=api))
                info = str("")
            else:
                timeline = str(f"{header}{info}")
                Tweet_msg(msg=timeline,api=api)
                info = str("")
        rank += 1

    if len(info) != 0:
        Tweet_msg(msg=info,api=api,reply_id=FecthLastestTweet(api=api))
        info = str("")

def ProvinceReport(api, data, data_vac):
    while True:
        index_data = Province_part(data, data_vac)

        ' Error Catching (When data from Province_part not match) [Testing ...] '
        # if index_data == 1:
        #     logging.warning("Rechecking.. Data is not equal")
        #     continue
        # else:
        #     SubReport(api,data,index_data)
        #     break
        
        SubReport(api, data, index_data)
        VaccineRankingReport(api, data_vac, index_data)
        break
    
# if __name__ == '__main__':
#     SubReportOverchar('central',data=requests.get("https://covid19.ddc.moph.go.th/api/Cases/today-cases-by-provinces").json()) #Test Panels