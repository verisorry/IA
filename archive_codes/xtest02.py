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
	points = []
	for col in range(width):
		for row in range(height):
			if img.getpixel((col, row)) == (1, 1, 1):
				points.append((col, row))
	points = list(set(points))
	points = sorted(points, key=lambda tup: tup[1])

	#sort into separate groups of coordinates
	dist = 53
	dist_sqr = dist**2
	def calc_distance(x1, y1, x2, y2):
		distance = (x2-x1)**2 + (y2-y1)**2
		return distance
	for i in range(len(points)-1):
		distance = calc_distance(points[i][0], points[i][1], points[i+1][0], points[i+1][1])
		if distance > dist_sqr:
			q1 = points[:i+1]
			q2 = points[i+1:]
	top1 = min(q1)
	top2 = min(q2)

	#find bottom coordinate of marks 
for x in range(1, 2):
	img = Image.open("cropped/cropped"+str(x)+'.jpg')
	width, height = img.size
	points = []
	for col in range(width):
		for row in range(height):
			if img.getpixel((col, row)) == (1, 1, 1):
				points.append((col, row))
	points = list(set(points))
	points = sorted(points, key=lambda tup: tup[1])



	
	#crop from original image and save as new file
	"""code"""