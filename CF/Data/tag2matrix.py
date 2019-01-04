#-*-encoding:utf-8-*-
#这个文件用来生成M1,M2,M3矩阵,输入标签json文件即可
import sys
import json
import numpy as np
reload(sys)
sys.setdefaultencoding('utf-8')

raw_tag_path = "../../Crawler/hot_movie_tag.json"
predict_tag_path = "KNN_tag.json"
review_tag_path = "Review_hot_tag.json"
movie_id_path = "../../Crawler/hot_id.txt"
similar_relation_path = "similar_tag.json"

tag_id_dict = dict()
id_tag_dict = dict()

if __name__ == '__main__':
	tag_id_dict = dict()
	movie_id_list = []
	with open(movie_id_path) as f:
		for line in f.readlines():
			movie_id_list.append(line[:-1])

	with open(raw_tag_path) as f:
		raw_tag_dict = json.load(f)
	
	with open(review_tag_path) as f:
		review_tag_dict = json.load(f)

	for i,movie_id in enumerate(movie_id_list):
		for tag in raw_tag_dict[movie_id]:
			#matrix1[i][tag_id_dict[tag]] = 1
			if tag_id_dict.has_key(tag):
				continue
			tag_id_dict[tag] = len(tag_id_dict)

	with open('current_tag.txt','w') as f:
		for tag in tag_id_dict:
			id_tag_dict[tag_id_dict[tag]] = tag
		for i in range(len(tag_id_dict)):
			f.write(id_tag_dict[i])
			f.write('\n')





	matrix1 = np.zeros((len(raw_tag_dict),len(tag_id_dict)),dtype=np.int8)
	matrix2 = np.zeros((len(raw_tag_dict),len(tag_id_dict)),dtype=np.int8)
	matrix3 = np.zeros((len(raw_tag_dict),len(tag_id_dict)),dtype=np.int8)
	matrix4 = np.zeros((len(raw_tag_dict),len(tag_id_dict)),dtype=np.int8)
	similar_matrix = np.zeros((len(tag_id_dict),len(tag_id_dict)),dtype=np.float32)
	similar_index_matrix = np.zeros((len(tag_id_dict),len(tag_id_dict)),dtype=np.int8)
	with open('similar_tag.json') as f:
		contents = json.load(f)
		for tag in contents:
			if tag not in tag_id_dict:
				continue
			first_id = tag_id_dict[tag]
			for i in range(10):
				i = str(i)
				second_id = tag_id_dict[contents[tag][i][0]]
				similar_matrix[first_id][second_id] = float(contents[tag][i][1])
				similar_index_matrix[first_id][second_id] = 1

	for i,movie_id in enumerate(movie_id_list):
		for tag in raw_tag_dict[movie_id]:
			matrix1[i][tag_id_dict[tag]] = 1
		for tag in review_tag_dict[movie_id]:
			matrix2[i][tag_id_dict[tag]] = 1
	

	for i in range(matrix3.shape[0]):
		for j in range(matrix3.shape[1]):
			matrix3[i][j] = matrix1[i][j]+matrix2[i][j]
			matrix4[i][j] = 2*matrix1[i][j]+matrix2[i][j]

	np.savetxt('hot_matrix.txt',matrix1,fmt="%d")
	np.savetxt('review_matrix.txt',matrix2,fmt="%d")
	np.savetxt('mix_matrix1.txt',matrix3,fmt="%d")
	np.savetxt('mix_matrix2.txt',matrix4,fmt="%d")
	np.savetxt('similar_matrix.txt',similar_matrix,fmt="%.4f")
	np.savetxt('similar_index_matrix.txt',similar_index_matrix,fmt="%.4f")