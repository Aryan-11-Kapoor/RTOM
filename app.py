from secrets import choice
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
from PIL import Image
import numpy as np
import argparse
import imutils
import scipy.spatial as sp
from imutils import contours
from imutils import perspective
from scipy.spatial import distance as dist


def main():
    st.title('Object Measurement')
    st.image('https://miro.medium.com/max/568/1*Y1S4hciQTfrB3xJuk2remA.png',width=250)
        
    st.subheader("This app allows you to measure objects!!!")
    

    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("**select an option**")
    st.sidebar.write("")

    sidebar=["static image","Real Time"]
    choice=st.sidebar.selectbox("choose",sidebar)
    

    if choice =="static image":
        image_file=st.file_uploader(
            "upload image", type=['jpeg','png','jpg','webp']
        )

        if image_file:
            image=Image.open(image_file)
            def mp(x,y):
                return((x[0]+y[0])*0.5,(x[1]+y[1])*0.5)

            ap = argparse.ArgumentParser()
            ap.add_argument("-i", "--image", required=True,
                            )
            ap.add_argument("-w", "--width", type=float, required=True,
                )
            args = vars(ap.parse_args())
# load the image, convert it to grayscale, and blur it slightly
            image = cv2.imread(args["image"])
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)
# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
            edged = cv2.Canny(gray, 50, 100)
            edged = cv2.dilate(edged, None, iterations=1)
            edged = cv2.erode(edged, None, iterations=1)
# find contours in the edge map
            cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	            cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
# sort the contours from left-to-right and initialize the
# 'pixels per metric' calibration variable
            (cnts, _) = contours.sort_contours(cnts)
            pixelsPerMetric = None
# loop over the contours individually
            for c in cnts:
                if cv2.contourArea(c) < 250:
                    continue
	        
                orig = image.copy()
                box = cv2.minAreaRect(c)
                box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
                box = np.array(box, dtype="int")
	# order the points in the contour
                box = perspective.order_points(box)
                cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
	# loop over the original points and draw them



                for (x, y) in box:
                     cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)




        
                (upper_left, upper_right, bottom_right, bottom_left) = box
                (upper_left_upper_rightX, upper_left_upper_rightY) = mp(upper_left, upper_right)
                (bottom_left_bottom_rightX, bottom_left_bottom_rightY) = mp(bottom_left, bottom_right)
	# compute the mp 
                (upper_left_bottom_leftX, upper_left_bottom_leftY) = mp(upper_left, bottom_left)
                (upper_right_bottom_rightX, upper_right_bottom_rightY) = mp(upper_right, bottom_right)
	# draw the mps on the image
                cv2.circle(orig, (int(upper_left_upper_rightX), int(upper_left_upper_rightY)), 5, (255, 0, 0), -1)
                cv2.circle(orig, (int(bottom_left_bottom_rightX), int(bottom_left_bottom_rightY)), 5, (255, 0, 0), -1)
                cv2.circle(orig, (int(upper_left_bottom_leftX), int(upper_left_bottom_leftY)), 5, (255, 0, 0), -1)
                cv2.circle(orig, (int(upper_right_bottom_rightX), int(upper_right_bottom_rightY)), 5, (255, 0, 0), -1)
	# draw lines between the mps
                cv2.line(orig, (int(upper_left_upper_rightX), int(upper_left_upper_rightY)), (int(bottom_left_bottom_rightX), int(bottom_left_bottom_rightY)),
		                    (255, 0, 255), 2)
                cv2.line(orig, (int(upper_left_bottom_leftX), int(upper_left_bottom_leftY)), (int(upper_right_bottom_rightX), int(upper_right_bottom_rightY)),
		                    (255, 0, 255), 2)
        # compute the distance between the mps
                dA = dist.euclidean((upper_left_upper_rightX, upper_left_upper_rightY), (bottom_left_bottom_rightX, bottom_left_bottom_rightY))
                dB = dist.euclidean((upper_left_bottom_leftX, upper_left_bottom_leftY), (upper_right_bottom_rightX, upper_right_bottom_rightY))
	
                if pixelsPerMetric is None:
                    pixelsPerMetric = dB / args["width"]
                A=dA / pixelsPerMetric
                B=dB/pixelsPerMetric
                
        # draw the object sizes 
                cv2.putText(orig, "{:.1f}in".format(A),
		                (int(upper_left_upper_rightX - 15), int(upper_left_upper_rightY - 10)), cv2.FONT_HERSHEY_COMPLEX,
		                    0.65, (255, 255, 255), 2)
                cv2.putText(orig, "{:.1f}in".format(B),
		                (int(upper_right_bottom_rightX + 10), int(upper_right_bottom_rightY)), cv2.FONT_HERSHEY_COMPLEX,
		                    0.65, (255, 255, 255), 2)
	
                cv2.imshow("Image", orig)
                cv2.waitKey(0)
    





    if choice =="Real Time":
        cap = cv2.VideoCapture('http://192.168.1.10:8080/video')
        parameters = cv2.aruco.DetectorParameters_create()
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_100)
        st.image('https://miro.medium.com/max/568/1*Y1S4hciQTfrB3xJuk2remA.png')
        st.title("Real Time Object Measurement App")
        st.subheader("This app allows you to measure objects in real-time !!!")
        
        FRAME_WINDOW = st.image([])
        Frame = st.image([])
        circleframe = st.image([])

        sideb = st.sidebar
        check1 = sideb.button("Rectangle")
        check2 = sideb.button("Circle")
        check3 = sideb.button("Stop")

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
            if check1:
                getcontours(image,showCanny=True)
            elif check2:
                getcircles(image)
            elif check3:
                break
                cap.release()
                cv2.destroyAllWindows()
if __name__=="__main__":
    main()
        