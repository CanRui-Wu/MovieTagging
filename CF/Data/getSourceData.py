#-*-encoding:utf-8-*-
#用于生成供libsvm格式的文件或csv文件

import sys
import json
import os
reload(sys)
sys.setdefaultencoding('utf-8')

tag_id_dict = dict()
movie_tags_dict = dict()
sepical_movie_tags_dict = dict()
movie_rate_dict = dict()
movie_collect_dict = dict()
movie_comment_dict = dict()
movie_reviews_dict = dict()
movie_wish_dict = dict()
movie_year_dict = dict()
movie_rating_dict = dict()

sepical_hot_id_set = set()

sepical_hot_id_path = "/home/wucanrui/Desktop/毕业论文/Crawler/sepcial_hot_id.txt"
source_file_path = "/home/wucanrui/Desktop/毕业论文/Crawler/hot_movie_tag.json"
source_file_path2 = "../CBCF/tag.json"
source_file_path3 = "/home/wucanrui/Desktop/毕业论文/Crawler/sepcial_hot_movie_tag.json"
rate_directory = "/home/wucanrui/Desktop/毕业论文/Crawler/电影详细属性"

with open(sepical_hot_id_path) as f:
	for line in f.readlines():
		sepical_hot_id_set.add(line[:-1])

for filename in os.listdir(rate_directory):
	filename = rate_directory+"/"+filename
	with open(filename) as f:
		movie_list = json.load(f)["data"]
		for movie in movie_list:
			try:
				movie_rate_dict[movie["id"]] = float(movie["rating"]["average"])
			except:
				movie_rate_dict[movie["id"]] = 0
			try:
				movie_collect_dict[movie["id"]] = float(movie["collect_count"])
			except:
				movie_collect_dict[movie["id"]] = 0
			try:
				movie_comment_dict[movie["id"]] = float(movie["comments_count"])
			except:
				movie_comment_dict[movie["id"]] = 0
			try:
				movie_reviews_dict[movie["id"]] = float(movie["reviews_count"])
			except:
				movie_reviews_dict[movie["id"]] = 0
			try:
				movie_wish_dict[movie["id"]] = float(movie["wish_count"])
			except:
				movie_wish_dict[movie["id"]] = 0
			try:
				movie_year_dict[movie["id"]] = float(movie["year"])
			except:
				movie_year_dict[movie["id"]] = 0
			try:
				movie_rating_dict[movie["id"]] = float(movie["ratings_count"])
			except:
				movie_rating_dict[movie["id"]] = 0


with open('current_tag.txt') as f:
	for i,line in enumerate(f.readlines()):
		tag_id_dict[line.strip().decode('utf-8')] = i

with open(source_file_path) as f:
	contents = json.load(f)
	for movie_id in contents:
		if movie_id in sepical_hot_id_set:
			continue
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

with open(source_file_path3) as f:
	contents = json.load(f)
	for movie_id in contents:
		sepical_movie_tags_dict[movie_id] = []
		for tag in contents[movie_id]:
			sepical_movie_tags_dict[movie_id].append(tag_id_dict[tag])




with open('rate_train.svm','w') as f:
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


with open('collect_train.svm','w') as f:
	for movie_id in movie_tags_dict:
		result = ""
		result += str(movie_collect_dict[movie_id])
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

with open('comment_train.svm','w') as f:
	for movie_id in movie_tags_dict:
		result = ""
		result += str(movie_comment_dict[movie_id])
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

with open('reviews_train.svm','w') as f:
	for movie_id in movie_tags_dict:
		result = ""
		result += str(movie_reviews_dict[movie_id])
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

with open('wish_train.svm','w') as f:
	for movie_id in movie_tags_dict:
		result = ""
		result += str(movie_wish_dict[movie_id])
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


with open('year_train.svm','w') as f:
	for movie_id in movie_tags_dict:
		result = ""
		result += str(movie_year_dict[movie_id])
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


with open('rating_train.svm','w') as f:
	for movie_id in movie_tags_dict:
		result = ""
		result += str(movie_rating_dict[movie_id])
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

# with open('rate_test.svm','w') as f:
# 	for movie_id in sepical_movie_tags_dict:
# 		result = ""
# 		result += str(movie_rate_dict[movie_id])
# 		tag_list = [0 for i in range(len(tag_id_dict))]
# 		for index in sepical_movie_tags_dict[movie_id]:
# 			tag_list[index] = 1
# 		for i,indicator in enumerate(tag_list):
# 			if indicator == 1:
# 				result += " "
# 				result += str(i+1)
# 				result += ":"
# 				result += str(indicator)
# 		f.write(result)
# 		f.write('\n')

# with open('collect_test.svm','w') as f:
# 	for movie_id in sepical_movie_tags_dict:
# 		result = ""
# 		result += str(movie_collect_dict[movie_id])
# 		tag_list = [0 for i in range(len(tag_id_dict))]
# 		for index in sepical_movie_tags_dict[movie_id]:
# 			tag_list[index] = 1
# 		for i,indicator in enumerate(tag_list):
# 			if indicator == 1:
# 				result += " "
# 				result += str(i+1)
# 				result += ":"
# 				result += str(indicator)
# 		f.write(result)
# 		f.write('\n')

# with open('comment_test.svm','w') as f:
# 	for movie_id in sepical_movie_tags_dict:
# 		result = ""
# 		result += str(movie_comment_dict[movie_id])
# 		tag_list = [0 for i in range(len(tag_id_dict))]
# 		for index in sepical_movie_tags_dict[movie_id]:
# 			tag_list[index] = 1
# 		for i,indicator in enumerate(tag_list):
# 			if indicator == 1:
# 				result += " "
# 				result += str(i+1)
# 				result += ":"
# 				result += str(indicator)
# 		f.write(result)
# 		f.write('\n')

# with open('reviews_test.svm','w') as f:
# 	for movie_id in sepical_movie_tags_dict:
# 		result = ""
# 		result += str(movie_reviews_dict[movie_id])
# 		tag_list = [0 for i in range(len(tag_id_dict))]
# 		for index in sepical_movie_tags_dict[movie_id]:
# 			tag_list[index] = 1
# 		for i,indicator in enumerate(tag_list):
# 			if indicator == 1:
# 				result += " "
# 				result += str(i+1)
# 				result += ":"
# 				result += str(indicator)
# 		f.write(result)
# 		f.write('\n')

# with open('wish_test.svm','w') as f:
# 	for movie_id in sepical_movie_tags_dict:
# 		result = ""
# 		result += str(movie_wish_dict[movie_id])
# 		tag_list = [0 for i in range(len(tag_id_dict))]
# 		for index in sepical_movie_tags_dict[movie_id]:
# 			tag_list[index] = 1
# 		for i,indicator in enumerate(tag_list):
# 			if indicator == 1:
# 				result += " "
# 				result += str(i+1)
# 				result += ":"
# 				result += str(indicator)
# 		f.write(result)
# 		f.write('\n')


# with open('year_test.svm','w') as f:
# 	for movie_id in sepical_movie_tags_dict:
# 		result = ""
# 		result += str(movie_year_dict[movie_id])
# 		tag_list = [0 for i in range(len(tag_id_dict))]
# 		for index in sepical_movie_tags_dict[movie_id]:
# 			tag_list[index] = 1
# 		for i,indicator in enumerate(tag_list):
# 			if indicator == 1:
# 				result += " "
# 				result += str(i+1)
# 				result += ":"
# 				result += str(indicator)
# 		f.write(result)
# 		f.write('\n')


# with open('rating_test.svm','w') as f:
# 	for movie_id in sepical_movie_tags_dict:
# 		result = ""
# 		result += str(movie_rating_dict[movie_id])
# 		tag_list = [0 for i in range(len(tag_id_dict))]
# 		for index in sepical_movie_tags_dict[movie_id]:
# 			tag_list[index] = 1
# 		for i,indicator in enumerate(tag_list):
# 			if indicator == 1:
# 				result += " "
# 				result += str(i+1)
# 				result += ":"
# 				result += str(indicator)
# 		f.write(result)
# 		f.write('\n')
