import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

with open('all_tag_search.json') as f:
	movie_tag_dict = json.load(f)
	for movie_id in movie_tag_dict:
		movie_tag_dict[movie_id] = list(set(movie_tag_dict[movie_id]))

top250_id = set()
with open('top250.txt') as f:
	for line in f.readlines():
		top250_id.add(line[:-1].decode('utf-8'))

result = dict()
for movie_id in movie_tag_dict:
	if movie_id not in top250_id:
		continue
	result[movie_id] = movie_tag_dict[movie_id]

f = open('1.json','w')
f.write(json.dumps(result,ensure_ascii=False,sort_keys=True, indent=2))
f.close()