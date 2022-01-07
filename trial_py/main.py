import os, sys, cv2,re
import numpy as np

import time


import init, question, markscheme

def main_mac_question(qp):	
	paper_code = question.question_program(qp)
	os.system("clear")
	return paper_code

def main_mac_markscheme(ms, paper_code):
	markscheme.markscheme_program(ms, paper_code)
	os.system("clear")


def main_win():
	make_folder.io_win()

if __name__ == "__main__":
	os_req = init.start()
	os.system("clear")
	if os_req == True:
		qp = sys.argv[1]
		ms = sys.argv[2]
		start_time = time.time()
		paper_code = main_mac_question(qp)
		main_mac_markscheme(ms, paper_code)
		print(time.time()-start_time)
		#run darwin dependent
	else:
		main_win()
		#run win dependent