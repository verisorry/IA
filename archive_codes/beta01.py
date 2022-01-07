import cv2, re, os, sys, shutil
from pdf2image import convert_from_path
from pytesseract import pytesseract
from pytesseract import Output
from PIL import Image
import numpy as np
import time

# path_file = str(sys.argv[1])
path_file = "test1.pdf"
start_time = time.time()
pages = convert_from_path(path_file)
images = []
left = []
count = 0
for page in pages:
	newpath = r"/Users/silviafang/Desktop/csc/h3/csc IA/trial_py/archive_codes/og"
	os.path.dirname(path_file)
	newpath = r"og".format(os.path.dirname(path_file))
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	page.save("og/out" + str(count) + ".jpg", "JPEG")
	count += 1

for i in range(1, count):
	img = Image.open("og/out"+str(i)+".jpg")
	#crop footer 
	area = (1, 95, 1653, 2189)
	cropped_img = img.copy()
	cropped_img = cropped_img.crop(area)
	newpath = r"/Users/silviafang/Desktop/csc/h3/csc IA/trial_py/archive_codes/cropped"
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	cropped_img.save('cropped/cropped' + str(i) + '.jpg')
	images.append('cropped/cropped' + str(i) + '.jpg')

	#crop and save left tab
	area = (0,3,190,2094)
	left_tab = cropped_img.copy()
	left_tab = left_tab.crop(area)
	newpath = r"/Users/silviafang/Desktop/csc/h3/csc IA/trial_py/archive_codes/left"
	if not os.path.exists(newpath):
		os.makedirs(newpath)
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

# find top line of question numbers  
img = cv2.imread('left_long.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(thresh, blackAndWhiteImage) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(gray, -1, sharpen_kernel)

custom_config = r'-l eng --oem 3 --psm 6 outputbase digits'

data = pytesseract.image_to_data(sharpen, config=custom_config, output_type = Output.DICT)
for i in list(data):
	if i not in ["text", "height", "width", "top", "left"]:
		data.pop(i, None)
question_result = [(left, top, width, height, text) for left, top, width, height, text in zip(*data.values()) if text.isdigit()]
if list(question_result[0])[4] != '1':
	new_tuple = list(question_result[0])
	new_tuple[4] = '1'
	new_tuple = tuple(new_tuple)
	question_result[0] = new_tuple

#find bottom line of score numbers
img = Image.open("long.jpg")

custom_config = r'-c tessedit_char_whitelist=[]1234567890 --psm 11'
data = pytesseract.image_to_data(img, config=custom_config, output_type = Output.DICT)
for i in list(data):
	if i not in ["text", "height", "width", "top", "left"]:
		data.pop(i, None)
pattern = re.compile("\[([0-9]*?)\]")
score_result = [(left, top, width, height, text) for left, top, width, height, text in list(zip(*data.values())) if pattern.match(text)]

# print("question result", question_result, "\nscore result:", score_result)

#split coordinates of scores to be in between the question numbers 
# ie. between (1) and (2) there should be 2 scores
q_s_dict = {}

for q in range(len(question_result)-1):
	for s in range(len(score_result)):
		if question_result[q][1] < score_result[s][1] < question_result[q+1][1]:
			if question_result[q][4] in q_s_dict:
				q_s_dict[question_result[q][4]].append(score_result[s])
			else:
				q_s_dict[question_result[q][4]]= [score_result[s]]
		elif question_result[q+1][1] == question_result[-1][1] and question_result[-1][1] < score_result[s][1]:
			if question_result[-1][4] in q_s_dict:
				q_s_dict[question_result[-1][4]].append(score_result[s])
			else:
				q_s_dict[question_result[-1][4]]= [score_result[s]]

#crop based on question number (top) and last score (bottom) 
last_dict = q_s_dict.copy()
for key in last_dict:
	last_dict[key] = list(last_dict[key][-1])

newpath = r"/Users/silviafang/Desktop/csc/h3/csc IA/trial_py/archive_codes/Results"
if not os.path.exists(newpath):
	os.makedirs(newpath)

img = Image.open("long.jpg")
width, height = img.size
area = (0, 0, 0, 0)
for question in last_dict:
	new_area = (0, area[3], width, int(last_dict[question][1]+last_dict[question][3])+50)
	result = img.crop(new_area)
	result.save("Results/Q" + question + ".jpg")
	area = new_area

if os.path.exists("Results/Q0.jpg"):
	os.remove("Results/Q0.jpg")


shutil.rmtree("/Users/silviafang/Desktop/csc/h3/csc IA/trial_py/archive_codes/og")
shutil.rmtree("/Users/silviafang/Desktop/csc/h3/csc IA/trial_py/archive_codes/cropped")
shutil.rmtree("/Users/silviafang/Desktop/csc/h3/csc IA/trial_py/archive_codes/left")
os.remove("left_long.jpg")
os.remove("long.jpg")
print(time.time()-start_time)