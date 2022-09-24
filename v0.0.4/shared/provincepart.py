import requests

url = "https://covid19.ddc.moph.go.th/api/Cases/today-cases-by-provinces"
data = requests.get(url).json()

north_index = ['เชียงราย','เชียงใหม่','ลำปาง','ลำพูน','แม่ฮ่องสอน','พะเยา','น่าน','แพร่','อุตรดิตถ์','ตาก']
northeast_index = ['อำนาจเจริญ','บึงกาฬ','บุรีรัมย์','ชัยภูมิ','กาฬสินธุ์','ขอนแก่น','เลย','มหาสารคาม','มุกดาหาร'
,'นครพนม','นครราชสีมา','หนองบัวลำภู','หนองคาย','ร้อยเอ็ด','สกลนคร','ศรีสะเกษ','สุรินทร์','อุบลราชธานี','อุดรธานี','ยโสธร']
central_index = ['กรุงเทพมหานคร','พระนครศรีอยุธยา','ปทุมธานี','นนทบุรี','นครปฐม','สมุทรปราการ','อ่างทอง','ชัยนาท','ลพบุรี','สมุทรสงคราม','สมุทรสาคร'
,'สระบุรี','สิงห์บุรี','สุพรรณบุรี','นครนายก','กาญจนบุรี','ประจวบคีรีขันธ์','ราชบุรี','เพชรบุรี','สุโขทัย','พิจิตร','พิษณุโลก','กำแพงเพชร','เพชรบูรณ์','นครสวรรค์','อุทัยธานี']
east_index = ['จันทบุรี','ฉะเชิงเทรา','ชลบุรี','ตราด','ปราจีนบุรี','ระยอง','สระแก้ว']
south_index = ['กระบี่','ชุมพร','ตรัง','นครศรีธรรมราช','นราธิวาส','ปัตตานี','พังงา','พัทลุง','ภูเก็ต','ยะลา','ระนอง','สงขลา','สตูล','สุราษฎร์ธานี']

alldict = {}
north = []
northeast = []
central = []
east = []
south = []

def province_part():
    
    for pv in data:
        for n in north_index:
            if pv['province'] == n:
                north.append(data.index(pv))
                north_index.remove(n)
                break
        
        for ne in northeast_index:
            if pv['province'] == ne:
                northeast.append(data.index(pv))
                northeast_index.remove(ne)
                break
        
        for c in central_index:
            if pv['province'] == c:
                central.append(data.index(pv))
                central_index.remove(c)
                break
        
        for e in east_index:
            if pv['province'] == e:
                east.append(data.index(pv))
                east_index.remove(e)
                break
        
        for s in south_index:
            if pv['province'] == s:
                south.append(data.index(pv))
                south_index.remove(s)
                break

    alldict['north'] = north
    alldict['northeast'] = northeast
    alldict['central'] = central
    alldict['east'] = east
    alldict['south'] = south

    def sort(k):
        return data[k]['new_case']

    for i in alldict:
        alldict[i].sort(reverse=True,key=sort)

    return alldict