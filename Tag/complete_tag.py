import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


allow_tag = set()
with open('douban_tag.txt') as f:
	for line in f.readlines():
		allow_tag.add(line[:-1].decode('utf-8'))

# top_250_id = []
# print "Load Top 250 Movie Id"
# with open('top250.txt') as f:
# 	for line in f.readlines():
# 		top_250_id.append(line[:-1])
# top_250_id_set = set(top_250_id)


tag_movie_dict = dict()
movie_tag_dict = dict()
# for id in top_250_id_set:
# 	movie_tag_dict[id] = []

with open('tag_search_complete.json') as f:
	tag_movie_dict = json.load(f)
	for tag in tag_movie_dict:
		if tag not in allow_tag:
			continue
		for movie_id in tag_movie_dict[tag]:
			#if movie_id in top_250_id_set:
			if movie_tag_dict.has_key(movie_id):
				movie_tag_dict[movie_id].append(tag)
			else:
				movie_tag_dict[movie_id] = []
				movie_tag_dict[movie_id].append(tag)

with open('complete_all_tag.json','w') as f:
	f.write(json.dumps(movie_tag_dict,ensure_ascii=False,sort_keys=True, indent=2))
