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

for top250_id in top250_id_set:
	try:
		movie_tag_dict.pop(top250_id)
	except:
		print top250_id

with open('similar_film') as f:
	similar_film_dict = json.load(f)

tag_index_map = dict()
tag_index_list = []
with open('douban_tag.txt') as f:
	for i,line in enumerate(f.readlines()):
		tag_index_map[line[:-1].decode('utf-8')] = i
		tag_index_list.append(line[:-1].decode('utf-8'))

with open('tag_relation_top100.json') as f:
	tag_relation_dict = json.load(f)


final_result = dict()
for movie_id in similar_film_dict:
	similar_list = similar_film_dict[movie_id]
	temp = dict()
	for i in range(len(tag_index_map)):
		temp[i] = 0
	for each in similar_list:
		similar_movie_id,value = each
		for tag in movie_tag_dict[similar_movie_id]:
			try:
				temp[tag_index_map[tag]] += 1
			except:
				print tag
	
	print "Algorithm Start"

	# Algorithm 1
	while len(temp) != 200:
		target_index,target_value = min(temp.items(),key=lambda x:x[1])
		temp.pop(target_index)
		if float(target_value) == 0:
			continue
		for each in tag_relation_dict[str(target_index)].items():
			index,value = each
			if temp.has_key(int(index)):
				temp[int(index)] += float(value)*target_value
	
	result = []
	for key,value in temp.items():
		result.append(tag_index_list[key])
	final_result[movie_id] = result

f = open('../Metric/tagrank.json','w')
f.write(json.dumps(final_result,ensure_ascii=False,sort_keys=True, indent=2))
f.close()


