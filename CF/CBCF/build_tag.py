import numpy as np
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

movie_id_list = []
tag_list = []
movie_tag_dict = dict()
additional_tag_dict = dict()
with open('../../Crawler/hot_id.txt') as f:
	for line in f.readlines():
		movie_id_list.append(line[:-1])

with open('../Data/current_tag.txt') as f:
	for line in f.readlines():
		tag_list.append(line[:-1])

with open('../../Crawler/hot_movie_tag.json') as f:
	origin_tag = json.load(f)

movie_tag_matix = np.loadtxt("result_bsvd_200.txt")
for movie_index in range(movie_tag_matix.shape[0]):
	sort_dict = dict()
	for tag_index in range(movie_tag_matix.shape[1]):
		sort_dict[tag_index] = movie_tag_matix[movie_index][tag_index]
	result = sorted(sort_dict.items(),key=lambda x:x[1],reverse=True)
	temp = []
	additional = []
	for tag in result[:10]:
		temp.append(tag_list[tag[0]])
		if tag_list[tag[0]] not in origin_tag[movie_id_list[movie_index]]:
			additional.append(tag_list[tag[0]])
	movie_tag_dict[movie_id_list[movie_index]] = temp
	additional_tag_dict[movie_id_list[movie_index]] = additional

with open('tag.json','w') as f:
	f.write(json.dumps(movie_tag_dict,ensure_ascii=False,sort_keys=True, indent=2))

with open('addtional_tag.json','w') as f:
	f.write(json.dumps(additional_tag_dict,ensure_ascii=False,sort_keys=True, indent=2))
