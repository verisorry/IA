import cv2, csv, re
from pdf2image import convert_from_path
from pytesseract import pytesseract
from pytesseract import Output
from PIL import Image

pages = convert_from_path("0417_s20_qp_11.pdf")
images = []
left = []
count = 0
for page in pages:
	page.save("og/out" + str(count) + ".jpg", "JPEG")
	count += 1

for i in range(1, count):
	img = Image.open("og/out"+str(i)+".jpg")
	#crop footer 
	area = (1, 1, 1653, 2189)
	cropped_img = img.copy()
	cropped_img = cropped_img.crop(area)
	cropped_img.save('cropped/cropped' + str(i) + '.jpg')
	images.append('cropped/cropped' + str(i) + '.jpg')

	#crop and save left tab
	area = (0,3,196,2186)
	left_tab = cropped_img.copy()
	left_tab = left_tab.crop(area)
	left_tab.save('left/left_tab' + str(i) + '.jpg')
	left.append('left/left_tab' + str(i) + '.jpg')

#merge all cropped images into one long jpg for easier cropping
imgs = [Image.open(i) for i in images]
min_img_width = min(i.width for i in imgs)
total_height = 0

for i in range(len(images)):
    total_height += imgs[i].height

long = Image.new(imgs[0].mode, (min_img_width, total_height))
y=0
for img in imgs:
    long.paste(img, (0, y))
    y+= img.height
    if y>32767:
    	long.thumbnail([32767, 32767], Image.ANTIALIAS)
long.save('long.jpg')

#merge all question tabs into one long jpg
imgs = [Image.open(i) for i in left]
min_img_width = min(i.width for i in imgs)
total_height = 0

for i in range(len(left)):
    total_height += imgs[i].height

left_long = Image.new(imgs[0].mode, (min_img_width, total_height))
y = 0
for img in imgs:
    left_long.paste(img, (0, y))
    y += img.height
    if y>32767:
    	left_long.thumbnail([32767, 32767], Image.ANTIALIAS)
left_long.save('left_long.jpg')

# if y>32767:
# 	image = Image.open("left_long.jpg")
# 	image.thumbnail([32767, 32767], image.LANCZOS)
# 	image.save('left_long.jpg')

# # find top line of question numbers 
# img = Image.open("left/left_tab1.jpg")

# custom_config = r'--oem 3 --psm 6 outputbase digits'
# data = pytesseract.image_to_data(img, config=custom_config, output_type = Output.DICT)
# # print(data['text'][4])
# # print(data['left'][4], data['top'][4],data['width'][4], data['height'][4])
# # print("box = (139, 172), (139, 195), (149, 172), (149, 195)")
# for i in list(data):
# 	if i not in ["text", "height", "width", "top", "left"]:
# 		data.pop(i, None)
# question_result = [(left, top, width, height, text) for left, top, width, height, text in zip(*data.values()) if text.isdigit()]

# #find bottom line of score numbers
# img = Image.open("cropped/cropped1.jpg")
# custom_config = r'-c tessedit_char_whitelist=[]1234567890 --psm 11'
# data = pytesseract.image_to_data(img, config=custom_config, output_type = Output.DICT)
# for i in list(data):
# 	if i not in ["text", "height", "width", "top", "left"]:
# 		data.pop(i, None)
# pattern = re.compile("\[(.*?)\]")
# score_result = [(left, top, width, height, text) for left, top, width, height, text in list(zip(*data.values())) if pattern.match(text)]

# print("question result", question_result, "\nscore result:", score_result)

# find top line of question numbers 
img = Image.open("left_long.jpg")

custom_config = r'--oem 3 --psm 6 outputbase digits'
data = pytesseract.image_to_data(img, config=custom_config, output_type = Output.DICT)
for i in list(data):
	if i not in ["text", "height", "width", "top", "left"]:
		data.pop(i, None)
question_result = [(left, top, width, height, text) for left, top, width, height, text in zip(*data.values()) if text.isdigit()]

#find bottom line of score numbers
img = Image.open("long.jpg")

custom_config = r'-c tessedit_char_whitelist=[]1234567890 --psm 11'
data = pytesseract.image_to_data(img, config=custom_config, output_type = Output.DICT)
for i in list(data):
	if i not in ["text", "height", "width", "top", "left"]:
		data.pop(i, None)
pattern = re.compile("\[(.*?)\]")
score_result = [(left, top, width, height, text) for left, top, width, height, text in list(zip(*data.values())) if pattern.match(text)]

print("question result", question_result, "\nscore result:", score_result)

#split coordinates of scores to be in between the question numbers 
# ie. between (1) and (2) there should be 2 scores
q_s_dict = {}
count = 0
for q in range(len(question_result)-1):
	for s in range(len(score_result)):
		if question_result[q][1] < score_result[s][1] < question_result[q+1][1]:
			if question_result[q][4] in q_s_dict:
				q_s_dict[question_result[q][4]].append(score_result[s])
			else:
				q_s_dict[question_result[q][4]]= list(score_result[s])
print(q_s_dict)


#crop from original image and save as new file
#crop based on question number (top) and last score (bottom) 
"""code"""