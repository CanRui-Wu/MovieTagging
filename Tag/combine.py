import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

allow_set = set()
with open('douban_tag.txt') as f:
	for line in f.readlines():
		allow_set.add(line[:-1].decode('utf-8'))

with open('all_tag_search.json') as f:
	movie_tag_dict = json.load(f)

final_movie_tag_dict = dict()

with open('tfidf_tagweight_top250.json') as f:
	mannul_tag_dict = json.load(f)

for movie_id in movie_tag_dict:
	if not mannul_tag_dict.has_key(movie_id):
		continue
	temp = set(movie_tag_dict[movie_id])
	for tag in mannul_tag_dict[movie_id]:
		if len(temp) >= 100:
			break
		if tag in allow_set:
			temp.add(tag)
	final_movie_tag_dict[movie_id] = list(temp)

f = open('combine_tag.json','w')
f.write(json.dumps(final_movie_tag_dict,ensure_ascii=False,sort_keys=True, indent=2))
f.close()

