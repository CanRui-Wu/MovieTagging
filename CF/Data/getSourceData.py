#-*-encoding:utf-8-*-
#用于生成供libsvm格式的文件或csv文件

import sys
import json
import os
reload(sys)
sys.setdefaultencoding('utf-8')

tag_id_dict = dict()
movie_tags_dict = dict()
movie_rate_dict = dict()
source_file_path = "/home/wucanrui/Desktop/毕业论文/Crawler/all_tag_search.json"
source_file_path2 = "Review_tag.json"
rate_directory = "/home/wucanrui/Desktop/毕业论文/Crawler/电影详细属性"

for filename in os.listdir(rate_directory):
	filename = rate_directory+"/"+filename
	with open(filename) as f:
		movie_list = json.load(f)["data"]
		for movie in movie_list:
			try:
				movie_rate_dict[movie["id"]] = float(movie["rating"]["average"])
			except:
				movie_rate_dict[movie["id"]] = 0

with open('allow_tag.txt') as f:
	for i,line in enumerate(f.readlines()):
		tag_id_dict[line.strip().decode('utf-8')] = i

with open(source_file_path) as f:
	contents = json.load(f)
	for movie_id in contents:
		movie_tags_dict[movie_id] = []
		for tag in contents[movie_id]:
			movie_tags_dict[movie_id].append(tag_id_dict[tag])

with open(source_file_path2) as f:
	contents = json.load(f)
	for movie_id in contents:
		for tag in contents[movie_id]:
			try:
				movie_tags_dict[movie_id].append(tag_id_dict[tag])
			except:
				continue

# with open('raw_tag.csv','w') as f:
# 	result = 'MovieID,Rate'
# 	for i in range(len(tag_id_dict)):
# 		result += ",Tag"
# 		result += str(i)
# 	f.write(result)
# 	f.write('\n')
# 	for movie_id in movie_tags_dict:
# 		result = movie_id
# 		result += ","
# 		result += str(movie_rate_dict[movie_id])
		
# 		tag_list = [0 for i in range(len(tag_id_dict))]
# 		for index in movie_tags_dict[movie_id]:
# 			tag_list[index] = 1
# 		for indicator in tag_list:
# 			result += ","
# 			result += str(indicator)
# 		f.write(result)
# 		f.write('\n')

with open('mix_tag.svm','w') as f:
	for movie_id in movie_tags_dict:
		result = ""
		result += str(movie_rate_dict[movie_id])
		tag_list = [0 for i in range(len(tag_id_dict))]
		for index in movie_tags_dict[movie_id]:
			tag_list[index] = 1
		for i,indicator in enumerate(tag_list):
			if indicator == 1:
				result += " "
				result += str(i+1)
				result += ":"
				result += str(indicator)
		f.write(result)
		f.write('\n')
