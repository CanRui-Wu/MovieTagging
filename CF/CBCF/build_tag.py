import numpy as np
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

movie_id_list = []
tag_list = []
movie_tag_dict = dict()
with open('../../Crawler/movie_id.txt') as f:
	for line in f.readlines():
		movie_id_list.append(line[:-1])

with open('../../Crawler/allow_tag.txt') as f:
	for line in f.readlines():
		tag_list.append(line[:-1])

movie_tag_matix = np.loadtxt("basic_svd_matrix_last.txt")
for movie_index in range(movie_tag_matix.shape[0]):
	sort_dict = dict()
	for tag_index in range(movie_tag_matix.shape[1]):
		sort_dict[tag_index] = movie_tag_matix[movie_index][tag_index]
	result = sorted(sort_dict.items(),key=lambda x:x[1],reverse=True)
	temp = []
	for tag in result[:20]:
		temp.append(tag_list[tag[0]])
	movie_tag_dict[movie_id_list[movie_index]] = temp

with open('basic_svd.json','w') as f:
	f.write(json.dumps(movie_tag_dict,ensure_ascii=False,sort_keys=True, indent=2))
