import word2vec
import time
import os
import re

if __name__ == '__main__':

	input_path  = "../crawler/data/"
	output_path = "./model/w2v_0506"

	# model = word2vec.w2v_model()
	# model.load_model(output_path)

	# file_list = os.listdir(input_path)
	#
	# file_pattern = re.compile(".\.txt")

	# for path in file_list:
	# 	if(file_pattern.search(path)):
	#
	# 		model.train(input_path+path)
	# 		model.save_model(output_path)
	#
	# 		t = time.localtime()
	#
	# 		g = open("train_log.txt","w")
	# 		g.write(path+str(" complete "))
	# 		g.write(' {}시{}분{}초\n'.format(t.tm_hour, t.tm_min, t.tm_sec))
	# 		g.close()

	# print(model.most_similar(["school","teacher"],[],20))
