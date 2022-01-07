import pytesseract,re, cv2
from pytesseract import Output

def question_OCR(width, i):
	img_path = "table/table{}.jpg".format(i)
	img = cv2.imread(img_path)
	height, _, _ = img.shape
	question_roi = img[0:height, 0:width].copy()

	custom_config = r"--oem 3 --psm 4"
	data = pytesseract.image_to_data(question_roi, config=custom_config, output_type = Output.DICT)

	for i in list(data):
		if i not in ["text", "height", "width", "top", "left"]:
			data.pop(i, None)

	pattern = re.compile("^[0-9]")
	question_result = [[left, top, width, height, text] for left, top, width, height, text in zip(*data.values()) if pattern.match(text)]
	for tup in question_result:
		tup.append(img_path)
	# print("question done")
	return question_result

def sort_questions(question_dict, question_result):
	key = int(question_result[0][4].split("(")[0])
	if key not in question_dict:
		question_dict[key] = question_result
	else:
		question_dict[key].append(question_result)
	# print("questions sorted")
	return question_dict
