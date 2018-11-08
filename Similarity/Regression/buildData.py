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
	movie_review_path = "../../Crawler/长评/"
	model_file_name = 'SummaryDoc2Vec'
	film_list = []
	count = 0

	top_250_id = set()
	# print "Load Top 250 Movie Id"
	# with open('top100.txt') as f:
	# 	for line in f.readlines():
	# 		top_250_id.add(line[:-1])

	print "Start loading Film Tag"
	f = open('../../Tag/all_tag_search.json')
	movie_tag_dict = json.load(f)
	f.close()

	print "Start loading Film"
	for i in range(21,100):
		f = open(movie_detail_path+str(i/10.0)+'.json')
		content = json.load(f)
		for film_content in content["data"]:
			try:
				movie_file = open(movie_review_path+str(i/10.0)+'/'+film_content["id"]+'.json')
			except:
				continue
			# if film_content["id"] in top_250_id:
			# 	continue
			if not movie_tag_dict.has_key(film_content["id"]) or len(movie_tag_dict[film_content["id"]]) < 20:
				continue
			tags = []
			if movie_tag_dict.has_key(film_content["id"]):
				tags = movie_tag_dict[film_content["id"]]
			film_list.append(film(film_content["title"],film_content["aka"],\
			film_content["casts"],film_content["directors"],film_content["genres"],\
			film_content["summary"],film_content["year"],film_content["id"],\
			film_content["countries"],film_content["rating"]["average"],count,tags))
			count += 1
		f.close()
	
	print "Totally use " + str(len(film_list)) + " movie"

	print "Start building model"
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
		model = gensim.models.Doc2Vec(dm=0,alpha=0.1,vector_size=2000,min_alpha=0.025,min_count=1,epochs=50)
		model.build_vocab(sentences)
		model.train(sentences,total_examples=model.corpus_count,epochs=model.epochs)
		model.save(model_file_name)

	f = open('pure_20tags.csv','w')
	f.write("Title,Countries,Cast,Director,Genre,Summary,Year,Tag\n")
	for i,film1 in enumerate(film_list):
		print i
		for j,film2 in enumerate(film_list[i+1:]):
			title_similarity,countries_similarity,cast_similarity,director_similarity,genre_similarity,tags_similarity,summary_similarity,year_diff = film1.getSimilarity(film2,model)
			result = str(title_similarity)+','+str(countries_similarity)+','+str(cast_similarity)+','+str(director_similarity)+','+str(genre_similarity)+','+str(summary_similarity)+','+\
			str(year_diff)+','+str(tags_similarity)+'\n'
			f.write(result)
	f.close()
