#-*-encoding:utf-8-*-
#这个文件用来生成M1,M2,M3矩阵,输入标签json文件即可
import sys
import json
import numpy as np

raw_tag_path = "../../Crawler/all_tag_search.json"
predict_tag_path = "../"
review_tag_path = "Review_tag.json"


if __name__ == '__main__':
	tag_id_dict = dict()


	with open('allow_tag.txt') as f:
		for i,line in enumerate(f.readlines()):
			tag_id_dict[line.strip().decode('utf-8')] = i

	with open(raw_tag_path) as f:
		raw_tag_dict = json.load(f)
	with open(review_tag_path) as f:
		review_tag_dict = json.load(f)

	if len(raw_tag_dict) != len(review_tag_dict):
		raise Exception("数量不同，请保证文件格式一致")

	matrix1 = np.zeros((len(raw_tag_dict),len(tag_id_dict)),dtype=np.int8)
	matrix2 = np.zeros((len(raw_tag_dict),len(tag_id_dict)),dtype=np.int8)
	matrix3 = np.zeros((len(raw_tag_dict),len(tag_id_dict)),dtype=np.int8)
	for i,movie_id in enumerate(sorted(raw_tag_dict.keys())):
		for tag in raw_tag_dict[movie_id]:
			matrix1[i][tag_id_dict[tag]] = 1

	for i,movie_id in enumerate(sorted(review_tag_dict.keys())):
		for tag in review_tag_dict[movie_id]:
			try:
				matrix3[i][tag_id_dict[tag]] = 1
			except:
				continue

	np.savetxt('matrix1.txt',matrix1,fmt="%d")
	np.savetxt('matrix3.txt',matrix3,fmt="%d")