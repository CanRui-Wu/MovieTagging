#-*-encoding:utf-8-*-
#这个文件用来生成M1,M2,M3矩阵,输入标签json文件即可
import sys
import json
import numpy as np

raw_tag_path = "../../Crawler/all_tag_search.json"
predict_tag_path = "KNN_tag.json"
review_tag_path = "Review_tag.json"
movie_id_path = "../../Crawler/movie_id.txt"
similar_tag_path = "similar_tag.json"


if __name__ == '__main__':
	tag_id_dict = dict()
	movie_id_list = []
	with open(movie_id_path) as f:
		for line in f.readlines():
			movie_id_list.append(line[:-1])

	with open('allow_tag.txt') as f:
		for i,line in enumerate(f.readlines()):
			tag_id_dict[line.strip().decode('utf-8')] = i

	with open(raw_tag_path) as f:
		raw_tag_dict = json.load(f)
	with open(review_tag_path) as f:
		review_tag_dict = json.load(f)
	with open(predict_tag_path) as f:
		predict_tag_dict = json.load(f)
	with open(similar_tag_path) as f:
		similar_tag_dict = json.load(f)




	if len(raw_tag_dict) != len(review_tag_dict) or len(predict_tag_dict) != len(raw_tag_dict):
		raise Exception("数量不同，请保证文件格式一致")

	matrix1 = np.zeros((len(raw_tag_dict),len(tag_id_dict)),dtype=np.int8)
	matrix2 = np.zeros((len(raw_tag_dict),len(tag_id_dict)),dtype=np.int8)
	matrix3 = np.zeros((len(raw_tag_dict),len(tag_id_dict)),dtype=np.int8)
	matrix4 = np.zeros((len(tag_id_dict),len(tag_id_dict)),dtype=np.float32)

	for tag1 in similar_tag_dict:
		id1 = tag_id_dict[tag1]
		for key in similar_tag_dict[tag1]:
			tag2 = similar_tag_dict[tag1][key][0]
			id2 = tag_id_dict[tag2]
			matrix4[id1][id2] = float(similar_tag_dict[tag1][key][1])
			print float(similar_tag_dict[tag1][key][1])

	# for i,movie_id in enumerate(movie_id_list):
	# 	for tag in raw_tag_dict[movie_id]:
	# 		matrix1[i][tag_id_dict[tag]] = 1

	# for i,movie_id in enumerate(movie_id_list):
	# 	for tag in predict_tag_dict[movie_id]:
	# 		try:
	# 			matrix2[i][tag_id_dict[tag]] = 1
	# 		except:
	# 			continue

	# for i,movie_id in enumerate(movie_id_list):
	# 	for tag in review_tag_dict[movie_id]:
	# 		try:
	# 			matrix3[i][tag_id_dict[tag]] = 1
	# 		except:
	# 			continue

	# for i in range(len(raw_tag_dict)):
	# 	for j in range(len(tag_id_dict)):
	# 		matrix2[i][j] += 2*matrix1[i][j]

	# np.savetxt('matrix1.txt',matrix1,fmt="%d")
	# np.savetxt('matrix2.txt',matrix2,fmt="%d")
	# np.savetxt('matrix3.txt',matrix3,fmt="%d")
	np.savetxt('matrix4.txt',matrix4,fmt="%.4f")