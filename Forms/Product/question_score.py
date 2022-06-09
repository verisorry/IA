import cv2
from pytesseract import Output 
import pytesseract, re

def question_OCR(img):
	height, width, channels = img.shape
	question_roi = img[0:height, 0:180].copy()
	custom_config = r"--oem 3 --psm 6 outputbase digits"
	data = pytesseract.image_to_data(question_roi, config=custom_config, output_type = Output.DICT)
	for i in list(data):
		if i not in ["text", "height", "width", "top", "left"]:
			data.pop(i, None)
	question_result = [(left, top, width, height, text) for left, top, width, height, text in zip(*data.values()) if text.isdigit()]
	return question_result

def score_OCR(img):
	height, width, channels = img.shape
	score_roi = img[0:height, 1474:1654].copy()
	custom_config = r'-c tessedit_char_whitelist=[]1234567890 --psm 11'
	data = pytesseract.image_to_data(score_roi, config=custom_config, output_type = Output.DICT)
	for i in list(data):
		if i not in ["text", "height", "width", "top", "left"]:
			data.pop(i, None)
	pattern = re.compile("\[(.*?)\]")
	score_result = [(left, top, width, height, text) for left, top, width, height, text in list(zip(*data.values())) if pattern.match(text)]
	return score_result

def find_q_s():
	img = cv2.imread('complete.jpg')
	question_result = question_OCR(img)
	score_result = score_OCR(img)
	return (question_result, score_result)
	