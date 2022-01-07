import cv2, os

def sorting_ms_dict(question_dict):
	pages_depth = []
	depth = lambda L: isinstance(L, list) and max(map(depth, L))+1
	for key in question_dict:
		page = depth(question_dict[key])
		pages_depth.append(page)

	for page in range(1, len(pages_depth)+1):
		if pages_depth[page-1] == 2:
			question_dict[page] = question_dict[page][-1]
		else:
			question_dict[page] = question_dict[page][-pages_depth[page-1]+1:]
			for x in range(1, pages_depth[page-1]-1):

				question_dict[page][x] = question_dict[page][x][-1]
	# print("ms dictionary sorted")
	return (question_dict, pages_depth)

def cropping_ms(paper_code, x, y, x2, y2, question_dict, pages_depth):
	if not os.path.exists("MSResults"):
		os.makedirs("MSResults")
	for key in question_dict:
		if pages_depth[key-1] > 2:
			for page in range(1, len(question_dict[key])):
				image = cv2.imread(question_dict[key][page][-1])
				height, width, _ = image.shape
				temp_y = y2-y
				wo_header = image[temp_y:height, 0:width]
				cv2.imwrite(question_dict[key][page][-1], wo_header)
			final = []
			for page in range(len(question_dict[key])):
				final.append(question_dict[key][page][-1])
			image = cv2.vconcat([cv2.imread(img) for img in final])

		else:
			image = cv2.imread(question_dict[key][-1])
		cv2.imwrite("MSResults/{}.jpg".format("_".join(paper_code)+"_Q" + str(key)), image)
		cv2.imshow("MSResults/{}.jpg".format("_".join(paper_code)+"_Q" + str(key)), image)
		# cv2.waitKey()





