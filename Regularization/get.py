#-*-encoding:utf-8-*-
import sys
import json
import os
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "Please input correct args"
		exit(1)
	source_file_path = sys.argv[1]
	tag_id_dict = dict()
	movie_id_directory = "/home/wucanrui/Desktop/毕业论文/Crawler/电影详细属性"
	movie_tags_dict = dict()

	with open(source_file_path) as f:
		contents = json.load(f)
		for movie_id in contents:
			movie_tags_dict[movie_id] = []
			for tag in contents[movie_id]:
				movie_tags_dict[movie_id].append(tag)

	movie_id_set = set()
	index = 0
	for filename in os.listdir(movie_id_directory):
		filename = movie_id_directory+"/"+filename
		with open(filename) as f:
			movie_list = json.load(f)["data"]
			for movie in movie_list:
				index += 1
				if movie["id"] in movie_id_set:
					print movie["id"]
				movie_id_set.add(movie["id"])
	
	print index
	print len(movie_id_set)
	new_movie_tags_dict = dict()
	for movie_id in movie_id_set:
		new_movie_tags_dict[movie_id] = []
		if movie_id in movie_tags_dict:
			new_movie_tags_dict[movie_id] = movie_tags_dict[movie_id]
			


	with open(source_file_path,'w') as f:
		f.write(json.dumps(new_movie_tags_dict,ensure_ascii=False,sort_keys=True,indent=2))