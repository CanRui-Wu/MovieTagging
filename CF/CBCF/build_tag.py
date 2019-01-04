import numpy as np
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

movie_id_list = []
sepcial_movie_id_list = set()
tag_list = []
movie_tag_dict = dict()
additional_tag_dict = dict()
parameter_list = [i for i in range(1,31)]

with open('../../Crawler/hot_id.txt') as f:
	for line in f.readlines():
		movie_id_list.append(line[:-1])

with open('../../Crawler/sepcial_hot_id.txt') as f:
	for line in f.readlines():
		sepcial_movie_id_list.add(line[:-1])

with open('../Data/current_tag.txt') as f:
	for line in f.readlines():
		tag_list.append(line[:-1])

with open('../../Crawler/hot_movie_tag.json') as f:
	origin_tag = json.load(f)

movie_tag_matix = np.loadtxt("2.txt")
for movie_index in range(movie_tag_matix.shape[0]):
	if movie_id_list[movie_index] in sepcial_movie_id_list:
		continue
	sort_dict = dict()
	for tag_index in range(movie_tag_matix.shape[1]):
		sort_dict[tag_index] = movie_tag_matix[movie_index][tag_index]
	result = sorted(sort_dict.items(),key=lambda x:x[1],reverse=True)
	temp = []
	additional = []
	for tag in result:
		if tag_list[tag[0]] not in origin_tag[movie_id_list[movie_index]]:
			temp.append(tag_list[tag[0]])
	movie_tag_dict[movie_id_list[movie_index]] = temp

for parameter in parameter_list:
	temp = dict()
	for movie_id in movie_tag_dict:
		temp[movie_id] = movie_tag_dict[movie_id][:parameter]
	with open('tag'+str(parameter)+'.json','w') as f:
		f.write(json.dumps(temp,ensure_ascii=False,sort_keys=True, indent=2))

