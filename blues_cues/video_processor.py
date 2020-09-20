import pyautogui
import cv2
import pytesseract  # for reading text
import time
import numpy as np
import imutils

## binarize
# retval2,threshold2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
# cv2.imwrite('../binarized.png', threshold2)

## detect text using pytesseract
# text = pytesseract.image_to_data('../binarized.png')
# print(text)

# image = pyautogui.screenshot()
# img = np.array(image)

def estimate_panel_size(img, debug=False):
	"""
	Uses edge detection / hough lines to estimate the size of a single
	video panel. 

	Returns (estimated width, estimated height).
	"""
	# binarize
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	binary = cv2.bitwise_not(gray) 
	output = np.zeros(img.shape, img.dtype)
	# detect edges
	edges = cv2.Canny(binary, 100, 200, output)
	if debug:
		cv2.imwrite('edges.jpg', edges) 
	lines = cv2.HoughLinesP(edges, 1, np.pi/180, 200)   # horizontal/vertical lines
	# store coords of lines
	a,b,c = lines.shape
	x_vals = set()
	y_vals = set()
	for i in range(a):
		x1, y1 = lines[i][0][:2]
		x2, y2 = lines[i][0][2:4]
		x_vals.add(x1)
		x_vals.add(x2)
		y_vals.add(y1)
		y_vals.add(y2)
	# estimate width and height of one panel from lines
	MIN_HEIGHT = img.shape[0] // 7
	MIN_WIDTH = img.shape[1] // 7
	est_height = None
	est_width = None
	for x1 in x_vals:
		for x2 in x_vals:
			diff = abs(x1-x2)
			if diff > MIN_WIDTH and (est_width is None or diff < est_width):
				est_width = diff

	for y1 in y_vals:
		for y2 in y_vals:
			diff = abs(y1-y2)
			if diff > MIN_HEIGHT and (est_height is None or diff < est_height):
				est_height = diff
	if debug:
		print("(W, H) = ({}, {})".format(est_width, est_height))
	
	return (est_width, est_height)

def count_muted(img, debug=False):
	"""
	Count the number of muted symbols in this image. 
	"""
	muted = cv2.imread('../muted_symbol.png')
	w, h = muted.shape[:2]

	found = set()
	threshold_dist = min(img.shape[0], img.shape[1]) // 7
	for scale in np.linspace(0.2, 1.0, 20)[::-1]:
		# resize the image according to the scale, and keep track
		# of the ratio of the resizing
		resized = imutils.resize(img, width = int(img.shape[1] * scale))
		r = img.shape[1] / float(resized.shape[1])
		# if the resized image is smaller than the template, then break
		# from the loop
		if resized.shape[0] < w or resized.shape[1] < h:
			break

		res = cv2.matchTemplate(img, muted, cv2.TM_CCOEFF_NORMED)
		threshold = 0.56
		loc = np.where(res >= threshold)

		for pt in zip(*loc[::-1]):
			cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
			found.add((pt[0], pt[1]))


	if debug:
		cv2.imwrite('matched.png', img)
	
	return len(found)

def estimate_camera_on_attendance(img1, img2, debug=False):
	"""
	Estimate the number of people who have their camera on.
	img1 and img2 are two cropped images showing just the zoom gallery view,
		and must be the same size. 

	Uses edge detection / hough lines to estimate the size of one person's
	video panel, then uses absolute diff and finds bounding boxes to estimate
	the number of panels that are in motion
	"""
	if (img1.shape[:2] != img2.shape[:2]):
		return

	est_width, est_height = estimate_panel_size(img1)
	
	# get absolute diff between images
	diff = img1.copy()
	cv2.absdiff(img1, img2, diff)
	gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
	for i in range(0, 3):
		dilated = cv2.dilate(gray.copy(), None, iterations= i+ 1)
	(T, threshold) = cv2.threshold(gray, 3, 255, cv2.THRESH_BINARY)
	if debug:
		cv2.imwrite("diff.png", threshold)

	if debug:
		print("naive estimate: {}".format(cv2.countNonZero(gray) / (gray.shape[0] * gray.shape[1])))

	# get bounding rectangles from diff
	(contours, hierarchy) = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	rectangles = list(map(cv2.boundingRect, contours))
	count = 0
	for x, y, w, h in rectangles:
		if w*h < est_width*est_height:
			continue
		count += (w*h) // (est_width*est_height)
		if debug:
			cv2.rectangle(img2, (x,y), (x+w,y+h), (0, 255, 0), 10)
	if debug:
		cv2.imwrite('rectangles.jpg', img2)
	total = (img1.shape[1] // est_height) * (img1.shape[0] // est_width)
	return min(count / total, 1)

if __name__ == "__main__":
	img1 = cv2.imread('../live_gallery_view_1.png')
	img2 = cv2.imread('../live_gallery_view_2.png')
	print(estimate_camera_on_attendance(img1, img2, debug=True))
	print(count_muted(cv2.imread('../zoom_gallery_view_test.png'), debug=True))

	image = pyautogui.screenshot()
	img = np.array(image)



#### EAST text detector
## Code inspired by:
## https://www.pyimagesearch.com/2018/08/20/opencv-text-detection-east-text-detector/

# resize to multiple of 32
# (newW, newH) = (320,320)
# image = cv2.resize(img, (newW, newH))
# (H, W) = img.shape[:2]

# layers = [
# 	"feature_fusion/Conv_7/Sigmoid",    # confidence scores
# 	"feature_fusion/concat_3",          # bounding box
# ]

# net = cv2.dnn.readNet("frozen_east_text_detection.pb")
# blob = cv2.dnn.blobFromImage(img, 1.0, (W, H),
# 	(123.68, 116.78, 103.94), swapRB=True, crop=False)
# net.setInput(blob)
# (scores, geometry) = net.forward(layers)

# (numRows, numCols) = scores.shape[2:4]
# rects = []
# confidences = []
# for y in range(0, numRows):
# 	# extract the scores (probabilities), followed by the geometrical
# 	# data used to derive potential bounding box coordinates that
# 	# surround text
# 	scoresData = scores[0, 0, y]
# 	xData0 = geometry[0, 0, y]
# 	xData1 = geometry[0, 1, y]
# 	xData2 = geometry[0, 2, y]
# 	xData3 = geometry[0, 3, y]
# 	anglesData = geometry[0, 4, y]