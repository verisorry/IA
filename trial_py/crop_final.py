#crop based on question number (top) and last score (bottom) 
import os, cv2, pytesseract
from PIL import Image
import cv2
import pytesseract

def output_crop(q_s_dict, output_type):
	code_image = cv2.imread("og/out3.jpg")
	paper_code_roi = code_image[2198:2339, 516:1151].copy()
	custom_config = "--oem 3 --psm 6"
	paper_code = pytesseract.image_to_string(paper_code_roi, config = custom_config, lang = "eng")
	if "_" in paper_code:
		paper_code = paper_code.split("_")
		paper_code.insert(3, "M")
		paper_code.insert(4, "J")
		paper_code[-2] = paper_code[-2][-2]
		paper_code = paper_code[1:-2]
		print(paper_code)
	elif "/" in paper_code:
		paper_code = paper_code.split("/")
		# print(paper_code)

	copy_dict = q_s_dict.copy()
	for key in copy_dict:
		copy_dict[key] = list(copy_dict[key][-1])

	if not os.path.exists("QPResults"):
		os.makedirs("QPResults")

	img = Image.open("complete.jpg")
	width, height = img.size
	area = (0, 0, 0, 0)

	for question in copy_dict:
		new_area = (0, area[3], width, int(copy_dict[question][1]+copy_dict[question][3])+50)
		result = img.crop(new_area)
		result.save("QPResults/"+"_".join(paper_code)+"_Q" + question + ".jpg")
		area = new_area
	return paper_code
