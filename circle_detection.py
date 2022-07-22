from math import pi
import cv2
import numpy as np
import math
cap = cv2.VideoCapture(0)




#reading image first
img=cv2.imread('circles1.png',cv2.IMREAD_UNCHANGED)

grey_scale=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

new_img=cv2.GaussianBlur(grey_scale,(5,5),cv2.BORDER_DEFAULT)


thresh, image_black = cv2.threshold(grey_scale, 100,120,cv2.THRESH_BINARY)
canny_img=cv2.Canny(new_img,100,120)
detected_circles=cv2.HoughCircles(new_img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=5,maxRadius=100)





if detected_circles is not None:
  
    # Convert the circle parameters a, b and r to integers.
    detected_circles = np.uint16(np.around(detected_circles))
  
    for i in detected_circles[0,:]:
        x,y,r=i[0],i[1],i[2]
        area=math.pi*int(r)*int(r)
        cv2.circle(img,(x,y),r,(0,255,0),2)#drawing circumference
        cv2.putText(img,"area: {}".format(round(area,2)),(int(x),int(y)),cv2.FONT_HERSHEY_PLAIN,1,(255,0,255),1,cv2.LINE_AA)
        cv2.imshow("circles",img)
#cv2.imshow("compare",numpy.hstack((grey_scale,new_img)))'''






cv2.waitKey(0)
cv2.destroyAllWindows()