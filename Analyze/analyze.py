#-*-encoding:utf-8-*-
import json
import os

with open('all_tag_search.json') as f:
	movie_tag_dict = json.load(f)

movie_review_dict = dict()

movie_detail_path = "../Crawler/电影详细属性/"


for file in os.listdir(movie_detail_path):
	f = open(movie_detail_path+file)
	content = json.load(f)
	for film_content in content["data"]:
		movie_review_dict[film_content["id"]] = int(film_content["reviews_count"])
	f.close()

result = dict()
count = dict()
for i in range(0,1000):
	result[i] = 0
	count[i] = 0

for movie_id in movie_tag_dict:
	try:
		group = int(movie_review_dict[movie_id]/20)
	except:
		continue
	result[group] += len(movie_tag_dict[movie_id])
	count[group] += 1


for i in range(0,1000):
	if count[i] != 0:
		result[i] /= float(count[i])
	print result[i],count[i]
