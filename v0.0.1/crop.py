import cv2

x=80
y=193
h=90
w=290

x1=510
y1=188
h1=95
w1=245

def croppic():
    print("[!] Process Data By CropPIC")
    img = cv2.imread("covid.png")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    (thresh, imgthreshold) = cv2.threshold(img, 210, 255, 1)
    return imgthreshold

# cv2.imshow('1',newinfect)
# cv2.imshow('2',newdeath)
# cv2.waitKey(0)