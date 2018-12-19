import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

current_tag = set()
current_id = set()
result = dict()

with open('current_tag.txt') as f:
	for line in f.readlines():
		current_tag.add(line[:-1].decode())

with open('../../Crawler/hot_id.txt') as f:
	for line in f.readlines():
		current_id.add(line[:-1])

with open('Review_tag.json') as f:
	contents = json.load(f)
	for movie_id in contents:
		if movie_id not in current_id:
			continue
		temp = []
		for tag in contents[movie_id]:
			if tag.decode() not in current_tag:
				continue
			temp.append(tag)
		result[movie_id] = temp

with open('Review_hot_tag.json','w') as f:
	f.write(json.dumps(result,ensure_ascii=False,sort_keys=True, indent=2))

