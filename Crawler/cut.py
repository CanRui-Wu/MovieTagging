import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

final_result = dict()
sepical_final_result = dict()
count = 0
sepical_count = 0
hot_id_list = []
sepcial_hot_id_list = []

with open('all_tag_search.json') as f:
	contents = json.load(f)
	for movie_id in contents:
		if len(contents[movie_id]) < 5:
			continue
		final_result[movie_id] = contents[movie_id]
		hot_id_list.append(movie_id)
		count += 1
		if len(contents[movie_id]) >= 30:
			sepical_final_result[movie_id] = contents[movie_id]
			sepcial_hot_id_list.append(movie_id)
			sepical_count += 1
		

print sepical_count
print count

with open('hot_movie_tag.json','w') as f:
	f.write(json.dumps(final_result,ensure_ascii=False,sort_keys=True, indent=2))

with open('sepcial_hot_movie_tag.json','w') as f:
	f.write(json.dumps(sepical_final_result,ensure_ascii=False,sort_keys=True, indent=2))

with open('hot_id.txt','w') as f:
	for movie_id in hot_id_list:
		f.write(movie_id)
		f.write('\n')

with open('sepcial_hot_id.txt','w') as f:
	for movie_id in sepcial_hot_id_list:
		f.write(movie_id)
		f.write('\n')
