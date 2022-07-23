#Measuring an object(image)
import numpy as np
import cv2



path = input("Enter the file name : ")
image=cv2.imread(path)

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

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
        area = cv2.contourArea(contour)

        #print(area)

        
        rect = cv2.minAreaRect(contour)
        (x,y), (w,h), angle = rect

        box = cv2.boxPoints(rect)
        box = np.int0(box)

        Wi = w*0.02645833  #converting from pixels to cm
        He = h*0.02645833

        cv2.polylines(image,[box],True,(0,255,0),2)
        cv2.putText(image,"Width : {}cm".format(round(Wi,1)),(int(x-100),int(y-100)), cv2.FONT_HERSHEY_PLAIN,2,(0,0,100),3)
        cv2.putText(image,"Height : {}cm".format(round(He,1)),(int(x-100),int(y)), cv2.FONT_HERSHEY_PLAIN,2,(0,0,100),3)
        print(box)

def getcircles(img):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_blurred = cv2.blur(gray, (3, 3))
            detected_circles = cv2.HoughCircles(gray_blurred,
                        cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                    param2 = 30, minRadius = 1, maxRadius = 40)
            cv2.imshow('im',detected_circles)

            # Convert the circle parameters a, b and r to integers.
            detected_circles = np.uint16(np.around(detected_circles))
            cv2.imshow('im',detected_circles)
            for pt in detected_circles[0, :]:
                
                    a, b, r = pt[0], pt[1], pt[2]
                    area = 3.14159*pt[2]*pt[2]
                    if area>1000:
                    # Draw the circumference of the circle.
                        cv2.circle(img, (a, b), r, (0, 255, 0), 2)
                        
                        cv2.putText(img,"Width : {}".format(round(r,1)),org =(0,100), fontFace = cv2.FONT_HERSHEY_PLAIN,fontScale = 1,color = (100,0,0),thickness = 1)
                            # Draw a small circle (of radius 1) to show the center.
                        cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
                      
                        cv2.imshow('i',img)

def object_Det(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3))
    detected_circles = cv2.HoughCircles(gray_blurred,
                        cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                    param2 = 30, minRadius = 1, maxRadius = 40)

    if detected_circles is not None:
        getcircles(image)
        
    else:
        getcontours(image,showCanny=True)
        
img = object_Det(image)


cv2.waitKey(0)
