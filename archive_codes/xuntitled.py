import cv2, csv, re
from pdf2image import convert_from_path
from pytesseract import pytesseract
from pytesseract import Output
from PIL import Image

pages = convert_from_path("0417_s20_qp_11.pdf")
images = []
count = 0
for page in pages:
	page.save("og/out" + str(count) + ".jpg", "JPEG")
	images.append("og/out" + str(count) + ".jpg")
	count += 1

print(images)