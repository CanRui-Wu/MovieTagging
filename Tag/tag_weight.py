import json
import math
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

with open('all_tag_search.json') as f:
	movie_tag_dict = json.load(f)

top250_id_set = set()

with open('top250.txt') as f:
	for line in f.readlines():
		top250_id_set.add(line[:-1].decode('utf-8'))

tag_dict = dict()
for movie_id in movie_tag_dict:
	if movie_id in top250_id_set:
		continue
	for tag in movie_tag_dict[movie_id]:
		if tag_dict.has_key(tag):
			tag_dict[tag] += 1
		else:
			tag_dict[tag] = 1

for tag in tag_dict:
	tag_dict[tag] = math.log(float(tag_dict[tag]))

f = open('tag_weight.json','w')
f.write(json.dumps(tag_dict,ensure_ascii=False,sort_keys=True, indent=2))
f.close()

