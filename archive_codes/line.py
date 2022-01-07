from PIL import Image, ImageDraw
import trial

im = trial.img
draw = ImageDraw.Draw(im)
#1477, 1933, 32, 29
#left, top, width, height
for i in range(len(trial.question_result)):
	var = trial.question_result[i]
	bottomleft_x = var[0]
	bottomleft_y = var[1]+var[3]
	bottomright_x = var[0] + var[2]
	bottomright_y = bottomleft_y
	draw.line((bottomleft_x, bottomleft_y, bottomright_x, bottomright_y), fill = 128)
for i in range(len(trial.score_result)):
	var = trial.score_result[i]
	bottomleft_x = var[0]
	bottomleft_y = var[1]+var[3]
	bottomright_x = var[0] + var[2]
	bottomright_y = bottomleft_y
	draw.line((bottomleft_x, bottomleft_y, bottomright_x, bottomright_y), fill = 128)
im.show()

# left_x = trial.result[0][]
# left_y =
# right_x = 
# right_y = 
# draw.line((1477, 1172, 1509, 1172), fill = 128)
# draw.line((411, 1312, 493, 1312), fill = 128)
# draw.line((1477, 1962, 1509, 1962), fill = 128)
# im.show()
