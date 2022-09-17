from decimal import Decimal
import os
import cv2
import numpy as np
from rentassist.settings import BASE_DIR

#######   training part    ###############
sample_path = os.path.join(BASE_DIR, 'apps/ocr/data/generalsamples.data')
responses_path = os.path.join(BASE_DIR, 'apps/ocr/data/generalresponses.data')

samples = np.loadtxt(sample_path, np.float32)
responses = np.loadtxt(responses_path, np.float32)
responses = responses.reshape((responses.size, 1))

model = cv2.ml.KNearest_create()
model.train(samples, cv2.ml.ROW_SAMPLE, responses)

############################# testing part  #########################


def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)


def ocr(image):
    im = cv2.imread(image)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
    
    contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
    contours,_ = sort_contours(contours, method='left-to-right')
    reading = ''
    for cnt in contours:
        if cv2.contourArea(cnt) > 70:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if  h > 56 and h < 100:  
                cv2.rectangle(im, (x -1, y-1), (x + 1 + w, y + 1 + h), (0, 255, 0), 1)
                roi = thresh[y:y + h, x:x + w]
                roismall = cv2.resize(roi, (10, 10))
                roismall = roismall.reshape((1, 100))
                roismall = np.float32(roismall)
                retval, results, neigh_resp, dists = model.findNearest(roismall, k=1)
                string = str(int((results[0][0])))
                reading += string 
                # cv2.putText(out, string, (x, y + h), 0, 1, (0, 255, 255))
    
    if len(reading) > 6:
        reading = reading[:6]

    reading = Decimal(reading[:5] + '.' + reading[5:])
    return reading

    