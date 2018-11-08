#-*-encoding:utf-8-*-
import jieba
import os
import json
import random
import gensim
import multiprocessing
import numpy as np
from gensim.models.doc2vec import TaggedDocument
import sys
sys.path.append("..")
reload(sys)
sys.setdefaultencoding('utf-8')

class film:
	def __init__(self,title,aka,casts,directors,genres,summary,year,id,countries,score,index,tags): 
		self.title = title
		self.aka = aka
		self.casts = [cast["id"] for cast in casts]
		self.directors = [director["id"] for director in directors]
		self.genres = genres
		self.summary = summary
		self.countries = countries
		self.score = score
		self.tags = tags
		try:
			self.year = int(year)
		except:
			self.year = 0
		self.index = index
		self.id = id

	def Jaccard(self,list_a,list_b):
		a = set(list_a)
		b = set(list_b)
		if len(a|b) == 0:
			return 0 
		return float(len(a&b))/len(a|b)

	def getSimilarity(self,film,model):
		countries_similarity = self.Jaccard(self.countries,film.countries)
		cast_similarity = self.Jaccard(self.casts,film.casts)
		director_similarity = self.Jaccard(self.directors,film.directors)
		genre_similarity = self.Jaccard(self.genres,film.genres)
		tags_similarity = self.Jaccard(self.tags,film.tags)
		summary_similarity = model.docvecs.similarity(self.index,film.index)
		title_similarity = model.docvecs.similarity(self.index+100000,film.index+100000)
		if summary_similarity < 0:
			summary_similarity = 0
		year_diff = abs(self.year-film.year)
		if year_diff > 100:
			year_diff = 0
		if tags_similarity != 0: #有影评的电影直接返回相似性
			return tags_similarity
		else: #无影评的电影预测其相似性
			return 0.139+0.025*title_similarity+0.019*countries_similarity+0.078*genre_similarity*0.084*summary_similarity


if __name__ == '__main__':
	movie_detail_path = "../Crawler/电影详细属性/"
	model_file_name = 'SummaryDoc2Vec'

	main_alogrithm_control = 1


	#豆瓣评分前250部电影用作测试集
	top_250_id = []
	print "Load Top 250 Movie Id"
	with open('top250.txt') as f:
		for line in f.readlines():
			top_250_id.append(line[:-1])
	top_250_id_set = set(top_250_id) #构建集合，用于加快查找速度

	#导入有影评的电影的标签
	print "Start loading Film Tag"
	f = open('combine_tag.json')
	movie_tag_dict = json.load(f)
	f.close()


	#导入每个标签的权重
	with open('tag_weight.json') as f:
		tag_weight_dict = json.load(f)

	#加载所有电影的所有属性及标签
	film_list = []
	top_250_film_list = []
	index = 0
	top_250_index = 0
	print "Start loading Film"

	tag_set = set() #用于记录所有可能的标签
	for file in os.listdir(movie_detail_path):
		f = open(movie_detail_path+file)
		content = json.load(f)
		for film_content in content["data"]:
			tags = []
			if film_content["id"] in top_250_id_set:
				top_250_film_list.append(film(film_content["title"],film_content["aka"],\
				film_content["casts"],film_content["directors"],film_content["genres"],\
				film_content["summary"],film_content["year"],film_content["id"],\
				film_content["countries"],film_content["rating"]["average"],top_250_index+200000,tags)) #200000用来区分测试集和训练集
				top_250_index += 1
				continue
			if movie_tag_dict.has_key(film_content["id"]):
				tags = movie_tag_dict[film_content["id"]]
			else: #Do not handle cold movie
				continue 
			for tag in tags:
				tag_set.add(tag)
			film_list.append(film(film_content["title"],film_content["aka"],\
			film_content["casts"],film_content["directors"],film_content["genres"],\
			film_content["summary"],film_content["year"],film_content["id"],\
			film_content["countries"],film_content["rating"]["average"],index,tags))
			index += 1
		f.close()




	print "Start building summary similarity model"
	model = None
	if os.path.exists(model_file_name):
		print "Model exist,start loading"
		model = gensim.models.Doc2Vec.load(model_file_name)
	else:
		print "Model does not exist,start Training"
		sentences = []
		for i in range(len(film_list)):
			sentences.append(TaggedDocument(words=list(jieba.cut(film_list[i].summary)),tags=[i]))
			sentences.append(TaggedDocument(words=list(jieba.cut(film_list[i].title)),tags=[i+100000]))
		for i in range(len(top_250_film_list)):
			sentences.append(TaggedDocument(words=list(jieba.cut(top_250_film_list[i].summary)),tags=[i+200000]))
			sentences.append(TaggedDocument(words=list(jieba.cut(top_250_film_list[i].title)),tags=[i+300000]))
		model = gensim.models.Doc2Vec(dm=0,alpha=0.1,vector_size=200,min_alpha=0.025,min_count=1,epochs=20)
		model.build_vocab(sentences)
		model.train(sentences,total_examples=model.corpus_count,epochs=model.epochs)
		model.save(model_file_name)


	#Addtional for other compare algorithm
	# tag_index_map = dict()
	# with open('douban_tag.txt') as f:
	# 	for i,line in enumerate(f.readlines()):
	# 		tag_index_map[line[:-1].decode('utf-8')] = i

	# final_result = []
	# genre_dict = dict()
	# country_dict = dict()
	# for n,film in enumerate(film_list):
	# 	temp = []
	# 	for country in film.countries[:2]:
	# 		if not country_dict.has_key(country):
	# 			country_dict[country] = len(country_dict)
	# 		temp.append(country_dict[country])
	# 	if len(film.countries) == 0:
	# 		temp.append(-1)
	# 		temp.append(-1)
	# 	elif len(film.countries) == 1:
	# 		temp.append(-1)
	# 	for genre in film.genres[:4]:
	# 		if not genre_dict.has_key(genre):
	# 			genre_dict[genre] = len(genre_dict)
	# 		temp.append(genre_dict[genre])
	# 	for i in range(4-len(film.genres)):
	# 		temp.append(-1)
	# 	for i in range(len(model.docvecs[n])):
	# 		temp.append(model.docvecs[n][i])
	# 	for i in range(len(model.docvecs[n+100000])):
	# 		temp.append(model.docvecs[n+100000][i])
	# 	tag_vector = [0 for i in range(len(tag_index_map))]
	# 	for tag in movie_tag_dict[film.id]:
	# 		if not tag_index_map.has_key(tag):
	# 			continue
	# 		tag_vector[tag_index_map[tag]] = 1
	# 		tag_set.add(tag_index_map[tag])
	# 	temp.extend(tag_vector)
	# 	final_result.append(temp)


	# f = open('film_embedded.csv','w')
	# temp = "Country1,Country2,Genre1,Genre2,Genre3,Genre4"
	# for i in range(200):
	# 	temp += ",Summary" + str(i+1)
	# for i in range(200):
	# 	temp += ",Title" + str(i+1)
	# for i in range(len(tag_index_map)):
	# 	temp += ",Tag" + str(i+1)
	# f.write(temp)
	# f.write('\n')
	# for result in final_result:
	# 	temp = str(result[0])
	# 	for each in result[1:]:
	# 		temp += ","+str(each)
	# 	f.write(temp)
	# 	f.write('\n')
	# f.close()

	# #top250
	# final_result = []
	# genre_dict = dict()
	# country_dict = dict()
	# for n,film in enumerate(top_250_film_list):
	# 	temp = []
	# 	for country in film.countries[:2]:
	# 		if not country_dict.has_key(country):
	# 			country_dict[country] = len(country_dict)
	# 		temp.append(country_dict[country])
	# 	if len(film.countries) == 0:
	# 		temp.append(-1)
	# 		temp.append(-1)
	# 	elif len(film.countries) == 1:
	# 		temp.append(-1)
	# 	for genre in film.genres[:4]:
	# 		if not genre_dict.has_key(genre):
	# 			genre_dict[genre] = len(genre_dict)
	# 		temp.append(genre_dict[genre])
	# 	for i in range(4-len(film.genres)):
	# 		temp.append(-1)
	# 	for i in range(len(model.docvecs[n+200000])):
	# 		temp.append(model.docvecs[n+200000][i])
	# 	for i in range(len(model.docvecs[n+300000])):
	# 		temp.append(model.docvecs[n+300000][i])
	# 	tag_vector = [0 for i in range(len(tag_index_map))]
	# 	for tag in movie_tag_dict[film.id]:
	# 		if not tag_index_map.has_key(tag):
	# 			continue
	# 		tag_vector[tag_index_map[tag]] = 1
	# 	temp.extend(tag_vector)
	# 	final_result.append(temp)

	# f = open('top250_film_embedded.csv','w')
	# temp = "Country1,Country2,Genre1,Genre2,Genre3,Genre4"
	# for i in range(200):
	# 	temp += ",Summary" + str(i+1)
	# for i in range(200):
	# 	temp += ",Title" + str(i+1)
	# for i in range(len(tag_index_map)):
	# 	temp += ",Tag" + str(i+1)
	# f.write(temp)
	# f.write('\n')
	# for result in final_result:
	# 	temp = str(result[0])
	# 	for each in result[1:]:
	# 		temp += ","+str(each)
	# 	f.write(temp)
	# 	f.write('\n')
	# f.close()

	# print "Finish embedding"
	top_250_result = dict()
	top_250_similarity = dict()
	for top_250_film in top_250_film_list:
		similarity_dict = dict()
		current_result_tag = dict()
		for i,film in enumerate(film_list):
			if film.id in top_250_id_set:
				continue
			similarity_dict[i] = top_250_film.getSimilarity(film,model)
		result = sorted(similarity_dict.items(),key = lambda x:x[1],reverse = True)[:100]
		temp = []
		for index,value in result:
			temp.append((film_list[index].id,value))
			if movie_tag_dict.has_key(film_list[index].id):
				for i,tag in enumerate(movie_tag_dict[film_list[index].id]):
					if current_result_tag.has_key(tag):
						current_result_tag[tag] += value
					else:
						current_result_tag[tag] = value

		top_250_similarity[top_250_film.id] = temp
		# current_result_tag = sorted(current_result_tag.items(),key = lambda x:x[1],reverse = True)[:200]
		# tag_list = []
		# print top_250_film.id
		# for tag,value in current_result_tag:
		# 	print tag,
		# 	tag_list.append(tag)
		# print ""
		# top_250_result[top_250_film.id] = tag_list

	# f = open('true_last_200.json','w')
	# f.write(json.dumps(top_250_result,ensure_ascii=False,sort_keys=True, indent=2))
	# f.close()
	f = open('../Tag/similar_film','w')
	f.write(json.dumps(top_250_similarity,ensure_ascii=False,sort_keys=True, indent=2))
	f.close()

