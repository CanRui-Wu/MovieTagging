import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

top250_id_set = set()
with open('top250.txt') as f:
	for line in f.readlines():
		top250_id_set.add(line[:-1].decode('utf-8'))

with open('all_tag_search.json') as f:
	movie_tag_dict = json.load(f)

result = dict()
result2 = dict()
for movie_id in movie_tag_dict:
	if movie_id in top250_id_set:
		result[movie_id] = movie_tag_dict[movie_id]
	else:
		result2[movie_id] = movie_tag_dict[movie_id]

f = open('top250_tag_search.json','w')
f.write(json.dumps(result,ensure_ascii=False,sort_keys=True, indent=2))
f.close()

f = open('other_tag_search.json','w')
f.write(json.dumps(result,ensure_ascii=False,sort_keys=True, indent=2))
f.close()
