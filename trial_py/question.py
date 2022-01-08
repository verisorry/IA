import make_folder, input_manipulation, question_score, qs_mainpulation, crop_final, cleaning

def question_program(qp, output_type):
	(images, count) = make_folder.io_mac(qp)
	(crop_bottom, count) = input_manipulation.tessa(images, count)
	(cropped, left) = input_manipulation.cropping(images, count, crop_bottom)
	input_manipulation.merge(cropped, left)
	(question_result, score_result) = question_score.find_q_s()
	q_s_dict = qs_mainpulation.sort_qs(question_result, score_result)
	paper_code = crop_final.output_crop(q_s_dict, "QP", output_type)
	cleaning.clean_up("QP")
	return paper_code
