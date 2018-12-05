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
			return 0.023+0.062*title_similarity+0.0949*genre_similarity+0.1273*summary_similarity


if __name__ == '__main__':
	movie_detail_path = "../Crawler/电影详细属性/"
	model_file_name = 'SummaryDoc2VecAll'


	print "Start loading Film Tag"
	f = open('../Crawler/all_tag_search.json')
	movie_tag_dict = json.load(f)
	f.close()


	#加载所有电影的所有属性及标签
	train_film_list = []
	test_film_list = []
	train_index = 0
	test_index = 0
	print "Start loading Film"
	for file in os.listdir(movie_detail_path):
		f = open(movie_detail_path+file)
		content = json.load(f)
		for film_content in content["data"]:
			tags = []
			if len(movie_tag_dict[film_content["id"]]) < 5:
				test_film_list.append(film(film_content["title"],film_content["aka"],\
				film_content["casts"],film_content["directors"],film_content["genres"],\
				film_content["summary"],film_content["year"],film_content["id"],\
				film_content["countries"],film_content["rating"]["average"],test_index+200000,tags)) #200000用来区分测试集和训练集
				test_index += 1
				continue
			else:
				train_film_list.append(film(film_content["title"],film_content["aka"],\
				film_content["casts"],film_content["directors"],film_content["genres"],\
				film_content["summary"],film_content["year"],film_content["id"],\
				film_content["countries"],film_content["rating"]["average"],train_index,tags))
				train_index += 1
		f.close()



	print "Start building summary similarity model"
	model = None
	if os.path.exists(model_file_name):
		print "Model exist,start loading"
		model = gensim.models.Doc2Vec.load(model_file_name)
	else:
		print "Model does not exist,start Training"
		sentences = []
		for i in range(len(train_film_list)):
			sentences.append(TaggedDocument(words=list(jieba.cut(train_film_list[i].summary)),tags=[i]))
			sentences.append(TaggedDocument(words=list(jieba.cut(train_film_list[i].title)),tags=[i+100000]))
		for i in range(len(test_film_list)):
			sentences.append(TaggedDocument(words=list(jieba.cut(test_film_list[i].summary)),tags=[i+200000]))
			sentences.append(TaggedDocument(words=list(jieba.cut(test_film_list[i].title)),tags=[i+300000]))
		model = gensim.models.Doc2Vec(dm=0,alpha=0.1,vector_size=200,min_alpha=0.025,min_count=1,epochs=20)
		model.build_vocab(sentences)
		model.train(sentences,total_examples=model.corpus_count,epochs=model.epochs)
		model.save(model_file_name)


	#Addtional for other compare algorithm
	tag_index_map = dict()
	with open('../Crawler/allow_tag.txt') as f:
		for i,line in enumerate(f.readlines()):
			tag_index_map[line[:-1].decode('utf-8')] = i

	final_result = []
	genre_dict = dict()
	country_dict = dict()
	print "Building genre dict and country dict"
	for n,film in enumerate(train_film_list):
		for country in film.countries:
			if not country_dict.has_key(country):
				country_dict[country] = len(country_dict)
		for genre in film.genres:
			if not genre_dict.has_key(genre):
				genre_dict[genre] = len(genre_dict)
	for n,film in enumerate(test_film_list):
		for country in film.countries:
			if not country_dict.has_key(country):
				country_dict[country] = len(country_dict)
		for genre in film.genres:
			if not genre_dict.has_key(genre):
				genre_dict[genre] = len(genre_dict)


	for n,film in enumerate(train_film_list):
		temp = []
		temp.append(film.id)
		country_vector = [0 for i in range(len(country_dict))]
		genre_vector = [0 for i in range(len(genre_dict))]
		for country in film.countries:
			country_vector[country_dict[country]] = 1

		for genre in film.genres:
			genre_vector[genre_dict[genre]] = 1
		temp.extend(country_vector)
		temp.extend(genre_vector)
		for i in range(len(model.docvecs[n])):
			temp.append(model.docvecs[n][i]/50)
		for i in range(len(model.docvecs[n+100000])):
			temp.append(model.docvecs[n+100000][i]/50)
		tag_vector = [0 for i in range(len(tag_index_map))]
		for tag in movie_tag_dict[film.id]:
			if not tag_index_map.has_key(tag):
				continue
			tag_vector[tag_index_map[tag]] = 1
		temp.extend(tag_vector)
		final_result.append(temp)


	f = open('train_film_embedded.csv','w')
	temp = "Id"

	for i in range(len(country_dict)):
		temp += ",Country" + str(i+1)
	for i in range(len(genre_dict)):
		temp += ",Genre" + str(i+1)
	for i in range(200):
		temp += ",Summary" + str(i+1)
	for i in range(200):
		temp += ",Title" + str(i+1)
	for i in range(len(tag_index_map)):
		temp += ",Tag" + str(i+1)
	f.write(temp)
	f.write('\n')
	for result in final_result:
		temp = str(result[0])
		for each in result[1:]:
			temp += ","+str(each)
		f.write(temp)
		f.write('\n')
	f.close()

	# test 
	final_result = []
	for n,film in enumerate(test_film_list):
		temp = []
		temp.append(film.id)
		country_vector = [0 for i in range(len(country_dict))]
		genre_vector = [0 for i in range(len(genre_dict))]
		for country in film.countries:
			country_vector[country_dict[country]] = 1

		for genre in film.genres:
			genre_vector[genre_dict[genre]] = 1
		temp.extend(country_vector)
		temp.extend(genre_vector)
		for i in range(len(model.docvecs[n])):
			temp.append(model.docvecs[n][i]/50)
		for i in range(len(model.docvecs[n+100000])):
			temp.append(model.docvecs[n+100000][i]/50)
		tag_vector = [0 for i in range(len(tag_index_map))]
		for tag in movie_tag_dict[film.id]:
			if not tag_index_map.has_key(tag):
				continue
			tag_vector[tag_index_map[tag]] = 1
		temp.extend(tag_vector)
		final_result.append(temp)

	f = open('test_film_embedded.csv','w')
	temp = "Id"
	for i in range(len(country_dict)):
		temp += ",Country" + str(i+1)
	for i in range(len(genre_dict)):
		temp += ",Genre" + str(i+1)
	for i in range(200):
		temp += ",Summary" + str(i+1)
	for i in range(200):
		temp += ",Title" + str(i+1)
	for i in range(len(tag_index_map)):
		temp += ",Tag" + str(i+1)
	f.write(temp)
	f.write('\n')
	for result in final_result:
		temp = str(result[0])
		for each in result[1:]:
			temp += ","+str(each)
		f.write(temp)
		f.write('\n')
	f.close()
