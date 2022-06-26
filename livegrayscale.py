import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    image_greyscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh, image_black = cv2.threshold(image_greyscale, 100,120,cv2.THRESH_BINARY)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    cv2.imshow('gray',image_black)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()