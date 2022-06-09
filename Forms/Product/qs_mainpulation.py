def sort_qs(question_result, score_result):
	q_s_dict = {}
	for q in range(len(question_result)-1):
		for s in range(len(score_result)):
			if question_result[q][1] < score_result[s][1] < question_result[q+1][1]:
				if question_result[q][4] in q_s_dict:
					q_s_dict[question_result[q][4]].append(score_result[s])
				else:
					q_s_dict[question_result[q][4]]= [score_result[s]]
			elif question_result[q+1][1] == question_result[-1][1] and question_result[-1][1] < score_result[s][1]:
				if question_result[-1][4] in q_s_dict:
					q_s_dict[question_result[-1][4]].append(score_result[s])
				else:
					q_s_dict[question_result[-1][4]]= [score_result[s]]
	return q_s_dict