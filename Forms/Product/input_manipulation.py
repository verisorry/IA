from PIL import Image
from pytesseract import Output
import numpy as np
import cv2, os, re, pytesseract

def tessa(images, count):
	crop_bottom = [None]
	for i in range(1, count):
		image = cv2.imread(images[i])
		custom_config = r'-c tessedit_char_whitelist=[]1234567890 --psm 11'
		data = pytesseract.image_to_data(image, output_type = Output.DICT, config=custom_config)
		for data_type in list(data):
			if data_type not in ["text", "height", "width", "top", "left"]:
				data.pop(data_type, None)
		pattern = re.compile("\[(.*?)\]")
		score_result = [(left, top, width, height, text) for left, top, width, height, text in list(zip(*data.values())) if pattern.match(text)]
		if len(score_result) == 0:
			crop_bottom.append(None)
			pass
		else:
			final_score = score_result[-1]
			crop_bottom.append(final_score[1]+final_score[3]+35)
	return crop_bottom, count

def cropping(images, count, crop_bottom):
	cropped, left = [], []
	for i in range(1, count):
		img = cv2.imread(images[i])
		if crop_bottom[i] == None:
			pass
		else:
			cropped_img = img[141:crop_bottom[i], 0:1654].copy()
			if not os.path.exists("cropped"):
				os.makedirs("cropped")
			cv2.imwrite("cropped/cropped" + str(i) + ".jpg", cropped_img)
			cropped.append('cropped/cropped' + str(i) + '.jpg')
			left_tab = img[141:crop_bottom[i], 0:201].copy()
			if not os.path.exists("left"):
				os.makedirs("left")
			cv2.imwrite('left/left_tab' + str(i) + '.jpg', left_tab)
			left.append('left/left_tab' + str(i) + '.jpg')
	return cropped, left

def merge(cropped, left):
	merged = cv2.vconcat([cv2.imread(img) for img in cropped])
	cv2.imwrite("complete.jpg", merged)
	merged = cv2.vconcat([cv2.imread(img) for img in left])
	cv2.imwrite("left_long.jpg", merged)
