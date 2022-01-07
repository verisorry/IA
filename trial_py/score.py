#find bottom line of score numbers
img = Image.open("long.jpg")

custom_config = r'-c tessedit_char_whitelist=[]1234567890 --psm 11'
data = pytesseract.image_to_data(img, config=custom_config, output_type = Output.DICT)
for i in list(data):
	if i not in ["text", "height", "width", "top", "left"]:
		data.pop(i, None)
pattern = re.compile("\[(.*?)\]")
score_result = [(left, top, width, height, text) for left, top, width, height, text in list(zip(*data.values())) if pattern.match(text)]