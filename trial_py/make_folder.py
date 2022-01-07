from pdf2image import convert_from_path
import sys, os

def io_mac(file_name):
	path_file = str(file_name)
	pages = convert_from_path(file_name)
	images = []
	count = 0
	for page in pages:
		newpath = r"og"
		if not os.path.exists(newpath):
			os.makedirs(newpath)
		page.save("og/out" + str(count) + ".jpg", "JPEG")
		images.append("og/out" + str(count) + ".jpg")
		count += 1
	# print("done mac")
	return (images, count)

def io_win(file_name):
	path_file = str(sys.argv[1])
	pages = convert_from_path(path_file)