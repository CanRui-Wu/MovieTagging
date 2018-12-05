# -*-encoding:utf-8-*-
import jieba
import os
import json
import random
import gensim
import math
import multiprocessing
from gensim.models.doc2vec import TaggedDocument
import sys
import numpy as np
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
		try:
			self.year = int(year)
		except:
			self.year = 0
		self.index = index
		self.id = id
		self.tags = tags

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
		return title_similarity,countries_similarity,cast_similarity,director_similarity,genre_similarity,tags_similarity,summary_similarity,year_diff

if __name__ == '__main__':
	movie_detail_path = "../../Crawler/电影详细属性/"
	model_file_name = 'SummaryAllDoc2Vec'
	film_list = []
	count = 0
	id_set = set()
	id_list = []
	id_all_list = []
	print "Start loading Film"
	for i in range(21,100):
		f = open(movie_detail_path+str(i/10.0)+'.json')
		content = json.load(f)
		tags = []
		for film_content in content["data"]:
			if film_content["id"] not in id_set:
				id_set.add(film_content["id"])
				id_list.append(film_content["id"])
			id_all_list.append(film_content["id"])
			film_list.append(film(film_content["title"],film_content["aka"],\
			film_content["casts"],film_content["directors"],film_content["genres"],\
			film_content["summary"],film_content["year"],film_content["id"],\
			film_content["countries"],film_content["rating"]["average"],count,tags))
			count += 1
		f.close()
	
	with open('movie_id_duplicate.txt','w') as f:
		for movie_id in id_all_list:
			f.write(movie_id)
			f.write('\n')

	with open('movie_id.txt','w') as f:
		for movie_id in id_list:
			f.write(movie_id)
			f.write('\n')

	# matrix = np.zeros((len(film_list),len(film_list)),dtype=np.float32)
	# print "Start building model"
	# model = None
	# if os.path.exists(model_file_name):
	# 	print "Model exist,start loading"
	# 	model = gensim.models.Doc2Vec.load(model_file_name)
	# else:
	# 	print "Model does not exist,start Training"
	# 	sentences = []
	# 	for i in range(len(film_list)):
	# 		sentences.append(TaggedDocument(words=list(jieba.cut(film_list[i].summary)),tags=[i]))
	# 		sentences.append(TaggedDocument(words=list(jieba.cut(film_list[i].title)),tags=[i+100000]))
	# 	model = gensim.models.Doc2Vec(dm=0,alpha=0.1,vector_size=2000,min_alpha=0.025,min_count=1,epochs=50)
	# 	model.build_vocab(sentences)
	# 	model.train(sentences,total_examples=model.corpus_count,epochs=model.epochs)
	# 	model.save(model_file_name)

	# for i,film1 in enumerate(film_list):
	# 	print i
	# 	for j,film2 in enumerate(film_list[i+1:]):
	# 		title_similarity,countries_similarity,cast_similarity,director_similarity,genre_similarity,tags_similarity,summary_similarity,year_diff = film1.getSimilarity(film2,model)
	# 		result = 0.023+0.062*title_similarity+0.0949*genre_similarity+0.1273*summary_similarity
	# 		matrix[i][j] = result
	# 		matrix[j][i] = result
	# np.savetxt('matrix.txt',matrix,fmt="%.4f")
