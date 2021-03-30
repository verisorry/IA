from pdf2image import convert_from_path

pages = convert_from_path("0417_s20_qp_11.pdf")

count = 0
for page in pages:
	page.save("og/out" + str(count) + ".jpg", "JPEG")
	count += 1

from PIL import Image
#1654 2339
for i in range(1, count):
	img = Image.open("og/out"+str(i)+".jpg")
	#crop footer 
	area = (1, 1, 1653, 2189)
	cropped_img = img.copy()
	cropped_img = cropped_img.crop(area)
	cropped_img.save('cropped/cropped' + str(i) + '.jpg')

	#crop and save left tab
	area = (0,3,196,2186)
	left_tab = cropped_img.copy()
	left_tab = left_tab.crop(area)
	left_tab.save('left/left_tab' + str(i) + '.jpg')

	#find top pixel of each question number
for x in range(1, 2):
	img = Image.open("left/left_tab"+str(x)+'.jpg')
	width, height = img.size
	x = []
	for col in range(width):
		for row in range(height):
			if img.getpixel((col, row)) == (1, 1, 1):
				x.append((col, row))
	x = list(set(x))
	x = sorted(x, key=lambda tup: tup[1])
	print(x)
	
	#crop from original image and save as new file
	"""code"""
