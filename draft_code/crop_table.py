import os, cv2, re
import numpy as np
import pytesseract
from pytesseract import Output

def check_GMP(images):
	for i in range(1, len(images)):
		image_path = "og/out{}.jpg".format(i)
		image = cv2.imread(image_path)
		data = pytesseract.image_to_string(image, config = "--oem 3 --psm 6", lang = "eng")

		if "Generic Marking Principles" not in data:
			return i
			break

def find_table(num):
	boxes = []
	image_path = "og/out{}.jpg".format(num)
	image = cv2.imread(image_path)

	gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	th1, img_bin = cv2.threshold(gray_scale, 150, 255, cv2.THRESH_BINARY)
	img_bin =~img_bin

	line_min_width = 50
	kernel_h = np.ones((1, line_min_width), np.uint8)
	kernel_v = np.ones((line_min_width,1), np.uint8)
	kernel = np.ones((20,1), np.uint8)
	  # note this is a horizontal kernel
	d_im = cv2.dilate(img_bin, kernel, iterations=1)
	e_im = cv2.erode(d_im, kernel, iterations=1) 

	img_bin_h = cv2.morphologyEx(e_im, cv2.MORPH_OPEN, kernel_h)
	img_bin_v = cv2.morphologyEx(e_im, cv2.MORPH_OPEN, kernel_v)
	img_bin_final = img_bin_h | img_bin_v

	_, _, stats, _ = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=4, ltype=cv2.CV_32S)

	for x,y,w,h,area in stats[2:]:
		roi = image[y:y+h, x:x+w].copy()
		custom_config = r"--oem 3 --psm 4"
		data = pytesseract.image_to_data(roi, config=custom_config, output_type = Output.DICT)
		for i in list(data):
			if i not in ["text", "height", "width", "top", "left"]:
				data.pop(i, None)

		pattern = re.compile("(Question?|Answer?|Marks?)")
		headings = [(text) for left, top, width, height, text in list(zip(*data.values())) if pattern.match(text)]

		boxes.append(((x, y, w, h, area), headings))
	# print("table found")
	return boxes


def sort_table(count_temp, boxes):
	new_count_temp = count_temp
	for stats, text in boxes:
		if text == ["Question"]:
			new_count_temp +=1
	box_dict = dict.fromkeys(range(count_temp, new_count_temp))		

	box_zip, end_zip = [], []
	col3_x, col3_w = 0, 0

	for (grid, text) in boxes:
		if text == ["Marks"]: 
			col3_x, col3_w = grid[0], grid[2]
		if text == ["Question"]:
			col3_x, col3_w = 0, 0
			box_zip.append([])
			end_zip.append([])
			box_zip[-1].append((grid, text))
		else:
			if grid[0] == col3_x and text != ["Marks"]:
				end_zip[-1].append((grid, text))

	i = 0
	for key in box_dict:
		box_dict[key] = box_zip[i]
		box_dict[key].append(end_zip[i])
		i+=1
	count_temp = new_count_temp
	# print("table sorted")
	return(count_temp, box_dict)


def cropping(page, box_dict, images):
	newpath = r"table"
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	for key in box_dict:
		new_image_path = "table/table{}.jpg".format(key)
		og_page = cv2.imread(images[page])
		top_left_x = box_dict[key][0][0][0]
		top_left_y = box_dict[key][0][0][1]
		bottom_right_x = box_dict[key][-1][-1][0][0]+box_dict[key][-1][-1][0][2]
		bottom_right_y = box_dict[key][-1][-1][0][1]+box_dict[key][-1][-1][0][3]
		new_image = og_page[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
		cv2.imwrite("{}".format(new_image_path), new_image)

	# print("cropped")
	return box_dict[key][0][0][2]

def save_header(box_dict, images):
	og_page = cv2.imread(images[3])
	for key in box_dict:
		top_left_x = box_dict[key][0][0][0]
		top_left_y = box_dict[key][0][0][1]
		bottom_right_x = box_dict[key][1][0][0][0]+box_dict[key][1][0][0][2]
		bottom_right_y = top_left_y+box_dict[key][0][0][3]
	header = og_page[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
	cv2.imwrite("table/header.jpg", header)
	# print("header saved")
	# print((top_left_x, top_left_y, bottom_right_x, bottom_right_y))
	return (top_left_x, top_left_y, bottom_right_x, bottom_right_y)


