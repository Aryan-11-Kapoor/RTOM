import numpy as np
import cv2
import streamlit as st
from PIL import Image


cap = cv2.VideoCapture('http://192.168.1.10:8080/video')
parameters = cv2.aruco.DetectorParameters_create()
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_100)



st.image('https://miro.medium.com/max/568/1*Y1S4hciQTfrB3xJuk2remA.png')
st.title("Real Time Object Measurement App")
st.subheader("This app allows you to measure objects in real-time !!!")
st.text("We use OpenCV and Streamlit for this demo")
FRAME_WINDOW = st.image([])
Frame = st.image([])
circleframe = st.image([])

def getcontours(img,cThr=[100,200],showCanny=False):
        
        image_greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_blur = cv2.GaussianBlur(image,(5,7),0)
        imagecanny = cv2.Canny(image_blur,cThr[0],cThr[1])
        kernel = np.ones((2,2))
        imgDial = cv2.dilate(imagecanny,kernel,iterations=3)
        imgThre = cv2.erode(imgDial,kernel,iterations=2)
        thresh, image_black = cv2.threshold(image_greyscale, 100,100,cv2.THRESH_BINARY)
        if showCanny : cv2.imshow('Canny',imgThre)
        cv2.imshow('canny',imgThre)
        
        
# Get Aruco marker
        corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    # Draw polygon around the marker
        if corners:
            int_corners = np.int0(corners)
            cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
            contours, _ = cv2.findContours(imgThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            aruco_perimeter = cv2.arcLength(corners[0], True)
            print(aruco_perimeter)
            pixel_cm_ratio = aruco_perimeter / 20
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 2500:
            
                    rect = cv2.minAreaRect(contour)
                    (x,y), (w,h), angle = rect


                    
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)

                    
                    wide =h/pixel_cm_ratio
                    tall =w/pixel_cm_ratio
                    cv2.circle(image,(int(x),int(y)),5,(0,0,255), -1)
                    cv2.polylines(image,[box],True,(0,255,0),2)
                    cv2.putText(image,"Width : {}".format(round(wide,1)),(int(x),int(y - 15)), cv2.FONT_HERSHEY_PLAIN,3,(0,0,100),3)
                    cv2.putText(image,"Height : {}".format(round(tall,1)),(int(x),int(y - 100)), cv2.FONT_HERSHEY_PLAIN,3,(0,0,100),3)
                    Frame.image(image)
            key = cv2.waitKey(1)
            
            if key == ord('s'): 
                cv2.imwrite(filename='saved_img.jpg', img=image)
                cap.release()    
        
def getcircles(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Blur using 3 * 3 kernel.
        gray_blurred = cv2.medianBlur(gray,5)
       
        corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
        if corners:
            int_corners = np.int0(corners)
            cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
            aruco_perimeter = cv2.arcLength(corners[0], True)
            print(aruco_perimeter)
            pixel_cm_ratio = aruco_perimeter / 20
            # Apply Hough transform on the blurred image.
            detected_circles = cv2.HoughCircles(gray_blurred,
                            cv2.HOUGH_GRADIENT, 1, 800, param1 = 50,
                        param2 = 70, minRadius = 1, maxRadius = 1000)

            
            # Draw circles that are detected.
            if detected_circles is not None:
                
                # Convert the circle parameters a, b and r to integers.
                detected_circles = np.uint16(np.around(detected_circles))

                for pt in detected_circles[0, :]:
                    
                        a, b, r = pt[0], pt[1], pt[2]
                        
                        print("radius : ",r)

                        if r>0:
                        # Draw the circumference of the circle.
                            cv2.circle(img, (a, b), r, (0, 255, 0), 2)
                            r=r/pixel_cm_ratio
                           
                            cv2.putText(img,"Width : {}".format(round(r,1)),org =(200,200), fontFace = cv2.FONT_HERSHEY_PLAIN,fontScale = 3,color = (100,0,0),thickness = 2)
                            # Draw a small circle (of radius 1) to show the center.
                            cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
                            circleframe.image(img)
            key = cv2.waitKey(1)


while(True):
    _, image = cap.read()
    FRAME_WINDOW.image(image) 
    getcontours(image,showCanny=True)
    
    getcircles(image)
                
    cv2.imshow('frame',image)
    

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
            

    # When everything done, release the capture
cap.release()
cv2.destroyAllWindows()