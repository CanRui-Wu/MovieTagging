#-*-encoding:utf-8-*-
import json
import os

with open('all_tag_search.json') as f:
	movie_tag_dict = json.load(f)

result = dict()
count = dict()
for i in range(40):
	result[i] = 0
	count[i] = 0

reviews_path = "../Crawler/长评/"
for i in range(20,99):
	score = i/10.0
	path = reviews_path + str(score)
	for filename in os.listdir(path):
		id = filename.split('.')[0]
		s = open(path+'/'+filename)
		h = json.load(s)
		if movie_tag_dict.has_key(id):
			count[len(movie_tag_dict[id])/5] += 1
			result[len(movie_tag_dict[id])/5] += len(h["data"]) 


for i in range(20):
	if count[i] == 0:
		print 0
	else:
		print result[i]/float(count[i])	

