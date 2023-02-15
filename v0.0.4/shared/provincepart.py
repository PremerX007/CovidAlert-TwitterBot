import collections

country = {
    'north'     : ['เชียงราย','เชียงใหม่','ลำปาง','ลำพูน','แม่ฮ่องสอน','พะเยา','น่าน','แพร่','อุตรดิตถ์','ตาก'],
    'northeast' : ['อำนาจเจริญ','บึงกาฬ','บุรีรัมย์','ชัยภูมิ','กาฬสินธุ์','ขอนแก่น','เลย','มหาสารคาม','มุกดาหาร','นครพนม','นครราชสีมา','หนองบัวลำภู','หนองคาย','ร้อยเอ็ด','สกลนคร','ศรีสะเกษ','สุรินทร์','อุบลราชธานี','อุดรธานี','ยโสธร'],
    'central'   : ['กรุงเทพมหานคร','พระนครศรีอยุธยา','ปทุมธานี','นนทบุรี','นครปฐม','สมุทรปราการ','อ่างทอง','ชัยนาท','ลพบุรี','สมุทรสงคราม','สมุทรสาคร','สระบุรี','สิงห์บุรี','สุพรรณบุรี','นครนายก','กาญจนบุรี','ประจวบคีรีขันธ์','ราชบุรี','เพชรบุรี','สุโขทัย','พิจิตร','พิษณุโลก','กำแพงเพชร','เพชรบูรณ์','นครสวรรค์','อุทัยธานี'],
    'east'      : ['จันทบุรี','ฉะเชิงเทรา','ชลบุรี','ตราด','ปราจีนบุรี','ระยอง','สระแก้ว'],
    'south'     : ['กระบี่','ชุมพร','ตรัง','นครศรีธรรมราช','นราธิวาส','ปัตตานี','พังงา','พัทลุง','ภูเก็ต','ยะลา','ระนอง','สงขลา','สตูล','สุราษฎร์ธานี']
}
            
alldict = {}
north = []
northeast = []
central = []
east = []
south = []
allzone = []

def checker(info):
    for zone in country:
        for province in country[zone]:
            if info['province'] == province: return zone
                
def province_part(data, data_vac):
    for info in data:
        temp = checker(info)
        if info['new_case'] != 0:
            if temp == 'north': north.append(data.index(info))
            elif temp == 'northeast': northeast.append(data.index(info))
            elif temp == 'central': central.append(data.index(info))
            elif temp == 'east': east.append(data.index(info))
            elif temp == 'south': south.append(data.index(info))
            else: pass
    
    for info in data_vac:
        temp = checker(info)
        if temp in ['north','northeast','central','east','south']: 
            if info['vaccine_total'] != 0: allzone.append(data_vac.index(info))

    ' Re-checking when does not match. [Testing..] '
    # if collections.Counter([data[x]['province'] for x in north]) != collections.Counter(country['north']): return 1 <<< USELESS

    for recheck in [data[x]['province'] for x in north]:
        if recheck not in country['north']: return 1 # <<<< ACTIVE

    alldict['north'] = north
    alldict['northeast'] = northeast
    alldict['central'] = central
    alldict['east'] = east
    alldict['south'] = south
    alldict['allzone'] = allzone
    
    def sorten_vac(k):
        return data_vac[k]['vaccine_total']

    def sorten(k):
        return data[k]['new_case']

    for i in alldict:
        if i == "allzone": 
            alldict[i].sort(reverse=True, key=sorten_vac) 
        else:
            alldict[i].sort(reverse=True, key=sorten)

    return alldict