import numpy as np
import cv2


ims = cv2.imread('phone.jpg')
image = cv2.imread('phone.jpg')
def getcontours(img,cThr=[100,100],showCanny=False):
    
    image_greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blur = cv2.GaussianBlur(image,(7,7),0)
    imagecanny = cv2.Canny(image_blur,cThr[0],cThr[1])
    kernel = np.ones((2,2))
    imgDial = cv2.dilate(imagecanny,kernel,iterations=3)
    imgThre = cv2.erode(imgDial,kernel,iterations=2)
    thresh, image_black = cv2.threshold(image_greyscale, 95,120,cv2.THRESH_BINARY)
    if showCanny : cv2.imshow('Canny',imgThre)
    contours, _ = cv2.findContours(imgThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    for contour in contours:

        rect = cv2.minAreaRect(contour)
        (x,y), (w,h), angle = rect

        box = cv2.boxPoints(rect)
        box = np.int0(box)

        Wi = w*0.02645833    #converting from pixels to cm
        He = h*0.02645833
        
        cv2.polylines(image,[box],True,(0,255,0),2)
        cv2.putText(image,"Width : {}cm".format(round(Wi,1)),(int(x-490),int(y - 15)), cv2.FONT_HERSHEY_PLAIN,3,(100,0,0),2)
        cv2.putText(image,"Height : {}cm".format(round(He,1)),(int(x-490),int(y - 100)), cv2.FONT_HERSHEY_PLAIN,3,(100,0,0),2)
        print(box)
    
            
getcontours(image,showCanny=True)
    
cv2.imshow('frame',image)
cv2.waitKey(0)
        
# When everything done, release the capture
cv2.destroyAllWindows()