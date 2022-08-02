import numpy as np
import cv2
import streamlit as st
from PIL import Image
import imutils
import scipy.spatial as sp
from imutils import contours
from imutils import perspective
from scipy.spatial import distance as dist
from badacc import *

def live():
    try:
        
        #cap = cv2.VideoCapture('http://192.168.25.243:8080/video')
        parameters = cv2.aruco.DetectorParameters_create()
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_100)
        user_input = st.text_input("Enter the URL of your IP Webcam:")
        cap = cv2.VideoCapture(user_input)
        st.markdown("###### URL format : http://your_ip_address:8080/video")
        st.markdown("###### Example URL : http://192.168.25.243:8080/video")
        options = st.radio("",('Start','Stop'))
        st.write("##### Choose the shape of the Object you want to measure")
        col1, col2 = st.columns([1,3])
        with col1:
            check1 = st.button("Rectangle/Square")
        with col2:
            check2 = st.button("Circle")
        #st.write("Enter the URL of your IP Webcam:")
        
        Frame = st.image([])
        circleframe = st.image([])
        FRAME_WINDOW = st.image([])
        
        
        #check3 = st.button("Stop")
        
        
        
    

        

        def getcontours(img,cThr=[100,200],showCanny=False):
                
                    _, image = cap.read()
                    
                    image_greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    image_blur = cv2.GaussianBlur(image,(5,7),0)
                    imagecanny = cv2.Canny(image_blur,cThr[0],cThr[1])
                    kernel = np.ones((2,2))
                    imgDial = cv2.dilate(imagecanny,kernel,iterations=3)
                    imgThre = cv2.erode(imgDial,kernel,iterations=2)
                    thresh, image_black = cv2.threshold(image_greyscale, 100,100,cv2.THRESH_BINARY)
                    
                    
                    
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
                                cv2.putText(image,"Width : {}".format(round(wide,2)),(int(x+135),int(y - 15)), cv2.FONT_HERSHEY_PLAIN,3,(0,0,100),3)
                                #st.empty(st.text(wide))
                                cv2.putText(image,"Height : {}".format(round(tall,2)),(int(x+135),int(y - 100)), cv2.FONT_HERSHEY_PLAIN,3,(0,0,100),3)
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
                                    
                                        cv2.putText(img,"Radius : {}".format(round(r,2)),org =(900,300), fontFace = cv2.FONT_HERSHEY_PLAIN,fontScale = 3,color = (100,0,0),thickness = 2)
                                        # Draw a small circle (of radius 1) to show the center.
                                        cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
                                        circleframe.image(img)
                                        
                                
                        key = cv2.waitKey(1)


        
        
        if options == 'Start':
            
            while True:
                _, image = cap.read()
                FRAME_WINDOW.image(image) 
                if check1:
                    getcontours(image,showCanny=True)
                elif check2:
                    getcircles(image)
        elif options == 'Stop':
                st.write("uuu")
                cap.release()
                cv2.destroyAllWindows()
                
    except:
        pass       
            
       


  