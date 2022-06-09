import os, shutil

def clean_up(out_type):
	if os.path.exists("{}Results/Q0.jpg".format(out_type)):
		os.remove("{}Results/Q0.jpg".format(out_type))
	shutil.rmtree("og")
	if out_type == "QP":
		os.remove("complete.jpg")
		os.remove("left_long.jpg")
		shutil.rmtree("cropped")
		shutil.rmtree("left")
	else:
		shutil.rmtree("table")