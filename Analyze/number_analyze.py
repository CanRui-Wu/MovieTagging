#-*-encoding:utf-8-*-
import json
import os

with open('all_tag_search.json') as f:
	movie_tag_dict = json.load(f)

result = dict()
for i in range(6):
	result[i] = 0

for movie_id in movie_tag_dict:
	number = len(movie_tag_dict[movie_id])/10
	if number > 5:
		number = 5
	result[number] += 1

for i in range(6):
	print result[i]



