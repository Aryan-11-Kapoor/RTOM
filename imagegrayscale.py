import numpy as np
import cv2

cap = cv2.VideoCapture(0)

ims = cv2.imread('object.jpg')
image=cv2.resize(ims,(960,740))
image_greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh, image_black = cv2.threshold(image_greyscale, 100,120,cv2.THRESH_BINARY)
#cv2.imshow('test.png',image)
#cv2.imshow('object.jpg', image_greyscale)
cv2.imshow('object.jpg',image_black)
cv2.waitKey(0)
cv2.destroyAllWindows()