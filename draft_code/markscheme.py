import make_folder, crop_table, read_question_ms, crop_ms, cleaning
import numpy as np

def markscheme_program(ms, paper_code):
	(images, count) = make_folder.io_mac(ms)
	ms_question_dict = {}
	count_temp = 1
	ms_start = crop_table.check_GMP(images)
	for ms_count in range(ms_start, len(images)):
		boxes = crop_table.find_table(ms_count)
		(count_temp, box_dict) = crop_table.sort_table(count_temp, boxes)
		ms_question_dict.update(box_dict)
		images = [images[index] for index in range(count)]
		width = crop_table.cropping(ms_count, box_dict, np.array(images))
	# print("tables all saved")
	(x, y, x2, y2) = crop_table.save_header(box_dict, images)
	question_dict = {}
	for ms_2_count in range(1,count_temp):
		question_result = read_question_ms.question_OCR(width, ms_2_count)
		question_dict = read_question_ms.sort_questions(question_dict, question_result)
	(question_dict, pages_depth) = crop_ms.sorting_ms_dict(question_dict)
	# print(question_dict)
	crop_ms.cropping_ms(paper_code, x, y, x2, y2, question_dict, pages_depth)
	cleaning.clean_up("MS")

# markscheme_program("test2_ms.pdf", ['0417', '11', 'M', 'J'])