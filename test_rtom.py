import numpy as np
import cv2


cap = cv2.VideoCapture(0)




while(True):
    _, image = cap.read()
    def getcontours(img,cThr=[100,100],showCanny=False):
        
        image_greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_blur = cv2.GaussianBlur(image,(7,7),0)
        imagecanny = cv2.Canny(image_blur,cThr[0],cThr[1])
        kernel = np.ones((2,2))
        imgDial = cv2.dilate(imagecanny,kernel,iterations=3)
        imgThre = cv2.erode(imgDial,kernel,iterations=2)
        thresh, image_black = cv2.threshold(image_greyscale, 145,120,cv2.THRESH_BINARY)
        if showCanny : cv2.imshow('Canny',imgThre)
        cv2.imshow('canny',imgThre)
        
        contours, _ = cv2.findContours(imgThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:
        
                rect = cv2.minAreaRect(contour)
                (x,y), (w,h), angle = rect


                
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                
                wide =w*0.02645833
                tall =h*0.02645833
                cv2.circle(image,(int(x),int(y)),5,(0,0,255), -1)
                cv2.polylines(image,[box],True,(0,255,0),2)
                cv2.putText(image,"Width : {}".format(round(wide,1)),(int(x),int(y - 15)), cv2.FONT_HERSHEY_PLAIN,1,(100,0,0),2)
                cv2.putText(image,"Height : {}".format(round(tall,1)),(int(x),int(y - 100)), cv2.FONT_HERSHEY_PLAIN,1,(100,0,0),2)
            key = cv2.waitKey(1)
            if key == ord('s'): 
                cv2.imwrite(filename='saved_img.jpg', img=image)
                cap.release()    
        
    def getcircles(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Blur using 3 * 3 kernel.
        gray_blurred = cv2.blur(gray, (3, 3))

        # Apply Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(gray_blurred,
                        cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                    param2 = 30, minRadius = 1, maxRadius = 40)

        
        # Draw circles that are detected.
        if detected_circles is not None:

            # Convert the circle parameters a, b and r to integers.
            detected_circles = np.uint16(np.around(detected_circles))

            for pt in detected_circles[0, :]:
                
                    a, b, r = pt[0], pt[1], pt[2]

                    # Draw the circumference of the circle.
                    cv2.circle(img, (a, b), r, (0, 255, 0), 2)
                    area = 3.14159*pt[2]*pt[2]
                    if area>3000:
                        cv2.putText(img,"Width : {}".format(round(r,1)),org =(200,200), fontFace = cv2.FONT_HERSHEY_PLAIN,fontScale = 1,color = (100,0,0),thickness = 2)
                        # Draw a small circle (of radius 1) to show the center.
                        cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
                    
        



    getcontours(image,showCanny=True)
    getcircles(image)
                
    cv2.imshow('frame',image)
    

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
            

    # When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
