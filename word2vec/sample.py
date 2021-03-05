import word2vec
import time
import os
import re

if __name__ == '__main__':

	input_path  = "../crawler/data/"
	output_path = "./model/w2v_0506"

	model = word2vec.w2v_model()
	model.load_model(output_path)

	file_list = os.listdir(input_path)

	file_pattern = re.compile(".\.txt")

	for path in file_list:
		if(file_pattern.search(path)):
			print(path)
