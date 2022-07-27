#Measuring an object(image)
from asyncio.windows_events import INFINITE
import numpy as np
import cv2



path = input("Enter the file name : ")
image=cv2.imread(path)



def getcontours(img,cThr=[100,100],showCanny=False):
    image_greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_blur = cv2.GaussianBlur(image,(7,7),0)
    imagecanny = cv2.Canny(image_blur,cThr[0],cThr[1])
    kernel = np.ones((2,2))
    imgDial = cv2.dilate(imagecanny,kernel,iterations=3)
    imgThre = cv2.erode(imgDial,kernel,iterations=2)
    thresh, image_black = cv2.threshold(image_greyscale, 95,120,cv2.THRESH_BINARY)
    if showCanny : cv2.imshow('Canny',imgThre)
    
    # Load Aruco detector
    parameters = cv2.aruco.DetectorParameters_create()
    aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
    ...
# Get Aruco marker
    corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    # Draw polygon around the marker
    int_corners = np.int0(corners)
    cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
    contours, _ = cv2.findContours(imgThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    aruco_perimeter = cv2.arcLength(corners[0], True)
    print(aruco_perimeter)
    pixel_cm_ratio = aruco_perimeter / 20
    for contour in contours:
        area = cv2.contourArea(contour)

        #print(area)

        
        rect = cv2.minAreaRect(contour)
        (x,y), (w,h), angle = rect

        box = cv2.boxPoints(rect)
        box = np.int0(box)

        Wi = w/pixel_cm_ratio  #converting from pixels to cm
        He = h/pixel_cm_ratio
        area = Wi*He
        if area>0:
            cv2.polylines(image,[box],True,(0,255,0),2)
            cv2.putText(image,"Width : {}cm".format(round(w,1)),(int(x-100),int(y-100)), cv2.FONT_HERSHEY_PLAIN,2,(0,0,100),3)
            cv2.putText(image,"Height : {}cm".format(round(He,1)),(int(x-100),int(y)), cv2.FONT_HERSHEY_PLAIN,2,(0,0,100),3)
            print(box)
        

def getcircles(img):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_blurred = cv2.GaussianBlur(gray,(5,5),0)
            
            detected_circles = cv2.HoughCircles(gray_blurred,
                        cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                    param2 = 30, minRadius = 10, maxRadius = 9000)
            
            

            # Convert the circle parameters a, b and r to integers.
            detected_circles = np.uint16(np.around(detected_circles))
           
            for pt in detected_circles[0, :]:
                
                    a, b, r = pt[0], pt[1], pt[2]
                    area = 3.14159*pt[2]*pt[2]
                    if r>1000:
                    # Draw the circumference of the circle.
                        cv2.circle(img, (a, b), r, (0, 255, 0), 2)
                        r = r*0.02645833
                        cv2.putText(img,"Width : {}".format(round(r,1)),org =(0,100), fontFace = cv2.FONT_HERSHEY_PLAIN,fontScale = 1,color = (100,0,0),thickness = 1)
                            # Draw a small circle (of radius 1) to show the center.
                        cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
                        
                        


getcircles(image)
    
getcontours(image,showCanny=True)
image = cv2.resize(image,(600,600))
cv2.imshow('img',image)       


cv2.waitKey(0)
