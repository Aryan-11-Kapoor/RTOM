import cv2
import numpy as np
import utlis

webcam = False
path='1.jpg'
cap=cv2.VideoCapture(0)
cap.set(10,160)
cap.set(3,1920)
cap.set(4,1080)
scale = 3
wP = 66*scale
hP = 132*scale


while True:
    if webcam: success,img = cap.read()
    else: img = cv2.imread(path)

    img, conts = utlis.getContours(img,minArea= 50000,filter=4)

    if len(conts)!= 0:
        biggest = conts[0][2]
        #print(biggest)
        imgWarp = utlis.warpImg(img, biggest, wP, hP)
        cv2.imshow('Phone', imgWarp)

    img = cv2.resize(img,(0,0),None,0.5,0.5)
    cv2.imshow('Original',img)
    cv2.waitKey(1)