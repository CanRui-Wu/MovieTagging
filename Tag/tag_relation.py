#-*-encoding:utf-8-*-
#This file is for candidate tag selection algorithm
import networkx as nx
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

with open('combine_tag.json') as f:
	movie_tag_dict = json.load(f)

top250_id_set = set()
with open('top250.txt') as f:
	for line in f.readlines():
		top250_id_set.add(line[:-1].decode('utf-8'))

for top250_id in top250_id_set:
	try:
		movie_tag_dict.pop(top250_id)
	except:
		print top250_id

tag_index_map = dict()
with open('douban_tag.txt') as f:
	for i,line in enumerate(f.readlines()):
		tag_index_map[line[:-1].decode('utf-8')] = i

G = nx.Graph()
G.add_nodes_from(range(0,len(tag_index_map)))
for i in range(len(tag_index_map)):
	for j in range(i,len(tag_index_map)):
		G.add_weighted_edges_from([(i,j,0)])


for movie_id in movie_tag_dict:
	if movie_id in top250_id_set: #Do not use test set to caculate weight
		continue
	tag_list = movie_tag_dict[movie_id]
	for i in range(len(tag_list)):
		for j in range(i+1,len(tag_list)):
			index1 = tag_index_map[tag_list[i]]
			index2 = tag_index_map[tag_list[j]]
			G[index1][index2]["weight"] += 1


tag_relation = dict()
for i in range(len(tag_index_map)):
	tag_relation[i] = dict()
	temp = dict()
	for j in range(len(tag_index_map)):
		temp[j] = G[i][j]["weight"]
	result = sorted(temp.items(),key=lambda x:x[1],reverse=True)[:30]
	total = 0
	for each in result:
		key,value = each
		total += value
	for each in result:
		key,value = each
		if total != 0:
			tag_relation[i][key] = float(value)/total #Normalize to 1
		else:
			tag_relation[i][key] = 0.1

f = open('tag_relation_top20.json','w')
f.write(json.dumps(tag_relation,ensure_ascii=False,sort_keys=True, indent=2))
f.close()

