import cv2
import numpy as np
import argparse
import imutils
import scipy.spatial as sp
from imutils import contours
from imutils import perspective
from scipy.spatial import distance as dist

def mp(x,y):
    return((x[0]+y[0])*0.5,(x[1]+y[1])*0.5)

#constructing the args parse and parsingF the args
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
	# if the contour is not sufficiently large, ignore it
	if cv2.contourArea(c) < 250:
		continue
	# compute the rotated bounding box of the contour
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
        
	(upper_left, upper_right, br, bl) = box
	(upper_left_upper_rightX, upper_left_upper_rightY) = mp(upper_left, upper_right)
	(blbrX, blbrY) = mp(bl, br)
	# compute the mp 
	(upper_leftblX, upper_leftblY) = mp(upper_left, bl)
	(upper_rightbrX, upper_rightbrY) = mp(upper_right, br)
	# draw the mps on the image
	cv2.circle(orig, (int(upper_left_upper_rightX), int(upper_left_upper_rightY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(upper_leftblX), int(upper_leftblY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(upper_rightbrX), int(upper_rightbrY)), 5, (255, 0, 0), -1)
	# draw lines between the mps
	cv2.line(orig, (int(upper_left_upper_rightX), int(upper_left_upper_rightY)), (int(blbrX), int(blbrY)),
		(255, 0, 255), 2)
	cv2.line(orig, (int(upper_leftblX), int(upper_leftblY)), (int(upper_rightbrX), int(upper_rightbrY)),
		(255, 0, 255), 2)
        # compute the distance between the mps
	dA = dist.euclidean((upper_left_upper_rightX, upper_left_upper_rightY), (blbrX, blbrY))
	dB = dist.euclidean((upper_leftblX, upper_leftblY), (upper_rightbrX, upper_rightbrY))
	
	if pixelsPerMetric is None:
		pixelsPerMetric = dB / args["width"]
        # compute the size of the object
	dimA = dA / pixelsPerMetric
	dimB = dB / pixelsPerMetric
	# draw the object sizes 
	cv2.putText(orig, "{:.1f}in".format(dimA),
		(int(upper_left_upper_rightX - 15), int(upper_left_upper_rightY - 10)), cv2.FONT_HERSHEY_PLAIN,
		0.65, (255, 255, 255), 2)
	cv2.putText(orig, "{:.1f}in".format(dimB),
		(int(upper_rightbrX + 10), int(upper_rightbrY)), cv2.FONT_HERSHEY_PLAIN,
		0.65, (255, 255, 255), 2)
	
	cv2.imshow("Image", orig)
	cv2.waitKey(0)