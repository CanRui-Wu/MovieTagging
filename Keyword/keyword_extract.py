# -*-encoding:utf-8-*-
import json
import sys
import os
from gensim.models import word2vec
import copy
import jieba
import math
from jieba import analyse
from math import sqrt
import jieba.posseg as pseg

reload(sys)
sys.setdefaultencoding('utf-8')
# model = word2vec.Word2Vec.load('Top250Word')
real_dir = os.path.split(os.path.realpath(__file__))[0]

analyse.set_idf_path(real_dir+"/idf_value.txt")
analyse.set_stop_words(real_dir+"/stop.txt")


class KeywordHandler:
	textrank = analyse.textrank
	tf_idf = analyse.extract_tags
	POS = ['ns','nt','nz','n','vn','an','a'] #词性限制为人名，地名，名词，动名词
	filter_set = set()
	allow_set = set()
	with open(real_dir+'/douban_tag.txt') as f:
		lines = f.readlines()
		for word in lines:
			allow_set.add(word[:-1].decode('utf-8'))

	print "Loading Idf Value"
	idf_dict = dict()
	with open(real_dir+'/idf_value.txt') as f:
		for line in f.readlines():
			word,value = line.split(' ')
			idf_dict[word.decode('utf-8')] = float(value)

	def __init__(self,number):
		self.all_content = []
		self.keywords = []
		self.keyword_number = number

	def setReviewPath(self,review_path):
		self.keywords = []
		self.all_content = []
		json_file = open(review_path)
		json_content = json.load(json_file)
		old_content = ""
		if len(json_content["data"]) == 0: #Film has no review
			return False
		for each in json_content["data"]: #There are some repeat reviews
			if old_content == each:
				continue
			old_content = each
			self.all_content.append(each.replace('\n',' '))
		return True

	def normalTextRank(self,type):
		self.keywords = []
		if type == 0: #将所有影评当成一个影评进行处理
			keywords_dict = dict()
			all_content = ""
			for content in self.all_content:
				all_content += content
			temp_keywords = self.textrank(all_content,topK=10000,withWeight=True)
			for keyword,value in temp_keywords:
				if keyword in self.allow_set:
						keywords_dict[keyword] = value
			
			sorted_result = sorted(keywords_dict.items(),key = lambda x:x[1],reverse=True)
			for keyword in sorted_result:
				if keyword[0] in self.allow_set:
					self.keywords.append(keyword[0])
		elif type == 1: #分开处理每一个影评再合并
			keywords = dict()
			for content in self.all_content:
				temp_keywords = self.textrank(content,topK=10000,withWeight=True,allowPOS=self.POS)
				temp_keywords = sorted(temp_keywords,key=lambda x:x[1],reverse=False)
				for i,keyword in enumerate(temp_keywords):
					if keywords.has_key(keyword[0]):
						keywords[keyword[0]] += (i+1.0)/len(temp_keywords)
					else:
						keywords[keyword[0]] = (i+1)*0.05

			for keyword,weight in sorted(keywords.items(),key=lambda x:x[1],reverse=True):
				if keyword in self.allow_set:
					self.keywords.append(keyword)
		elif type == 2: #textrank+idf
			all_content = ""
			for content in self.all_content:
				all_content += content
			temp_keywords = self.textrank(all_content, topK=10000,withWeight=True)
			temp = dict()
			for keyword,value in temp_keywords:
				try:
					temp[keyword] = value*self.idf_dict[keyword]
				except:
					temp[keyword] = value
			for keyword,weight in sorted(temp.items(),key=lambda x:x[1],reverse=True):
				if keyword in self.allow_set:
					self.keywords.append(keyword)
			
		return self.keywords[:self.keyword_number]


	def normalTfIDF(self,type):
		self.keywords = []
		if type == 0: #将所有影评当成一个影评进行处理
			all_content = ""
			for content in self.all_content:
				all_content += content
			temp_keywords = self.tf_idf(all_content,topK=100)
			for keyword in temp_keywords:
				if keyword in self.allow_set:
					self.keywords.append(keyword)
		elif type == 1: #分开处理每一个影评再合并
			keywords = dict()
			for content in self.all_content:
				temp_keywords = self.tf_idf(content,topK=10000,withWeight=True)
				temp_keywords = sorted(temp_keywords,key=lambda x:x[1],reverse=False)
				for i,keyword in enumerate(temp_keywords):
					if keywords.has_key(keyword[0]):
						keywords[keyword[0]] += (i+1.0)/len(temp_keywords)
					else:
						keywords[keyword[0]] = (i+1.0)/len(temp_keywords)
			sorted_result = sorted(keywords.items(),key = lambda x:x[1],reverse=True)
			for keyword in sorted_result:
				if keyword[0] in self.allow_set:
					self.keywords.append(keyword[0])
		elif type == 2:
			keywords_dict = dict()
			for keyword in self.allow_set:
				keywords_dict[keyword] = 0.0
			all_content = ""
			for content in self.all_content:
				all_content += content
			temp_keywords = self.tf_idf(all_content,topK=100)
			for i,keyword in enumerate(temp_keywords):
				weight = 1-float(i)/len(temp_keywords)
				if keyword in self.allow_set:
					keywords_dict[keyword] += weight
				else:
					try:
						for word,value in model.wv.most_similar(keyword,topn=10):
							if word in self.allow_set:
								keywords_dict[word] += weight*value
					except:
						continue
			sorted_result = sorted(keywords_dict.items(),key = lambda x:x[1],reverse=True)
			for keyword in sorted_result:
				if keyword[0] in self.allow_set:
					self.keywords.append(keyword[0])

		return self.keywords[:self.keyword_number]


	def superTextRank(self,window=5):
		self.keywords = []
		print "Super TextRanking"
		keywords = dict()
		for content in self.all_content:
			raw_words = pseg.dt.cut(content)
			graph = Graph(self.filter_set)
			words = []
			for word in raw_words:
				words.append(word)
			print "TextRanking"
			temp_keywords = graph.TextRank(words,self.POS,window)[:20]
			for i,keyword in enumerate(temp_keywords):
				if keywords.has_key(keyword[0]):
					keywords[keyword[0]] += 1 - math.log(1+(i/20)*(math.e-1))
				else:
					keywords[keyword[0]] = 1 - math.log(1+(i/20)*(math.e-1))

		sorted_result = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
		for keyword in sorted_result[:20]:
			self.keywords.append(keyword[0])



	def getAllPossible(self,file):
		self.keywords = []
		all_content = ''
		for content in self.all_content:
			all_content += content
		self.keywords = self.tf_idf(all_content,topK=200,allowPOS=self.POS)
		f = open(file,'w')
		for keyword in self.keywords[:200]:
			f.write(keyword)
			f.write('\n')
		f.close()

	def output(self):
		for keyword,weight in self.keywords:
			print keyword,weight

if __name__ == "__main__":
	reviews_path = "../Crawler/长评/"
	movie_detail_path = "../Crawler/电影详细属性/"
	main_algorithm_control = int(sys.argv[1])

	keyword_hd = KeywordHandler(100)
	method_name = ["tfidf","textrank+tag_weight","tfidf_split","textrank_split","textrank+idf","tfidf+tag_weight","tfidf","tfidf"]
	method = [(keyword_hd.normalTfIDF,0),(keyword_hd.normalTextRank,0),(keyword_hd.normalTfIDF,1),(keyword_hd.normalTextRank,1),(keyword_hd.normalTextRank,2),(keyword_hd.normalTfIDF,2),(keyword_hd.normalTfIDF,0),(keyword_hd.normalTfIDF,3)]
	method_file_list = ["tfidf_top250.json","textrank_tag_weight.json","tfidf_split_top250.json","textrank_split_top250.json","textrank_idf_split_top250.json","tfidf_wordsim_top250.json","tfidf_all.json","tfidf_tagweight_top250.json"]

	top_250_id = []
	print "Load Top 250 Movie Id"
	with open('top250.txt') as f:
		for line in f.readlines():
			top_250_id.append(line[:-1])
	top_250_id_set = set(top_250_id)

	print "Starting Generate Movie Tag"
	result_tag_dict = dict()
	
	

	print "Now running the algorithm " + method_name[main_algorithm_control]
	if os.path.exists(method_file_list[main_algorithm_control]):
		print "Previous tag exists,Start Loading"
		with open(method_file_list[main_algorithm_control]) as f:
			result_tag_dict = json.load(f)

	for i in range(20,99):
		score = i/10.0
		path = reviews_path + str(score)
		print path
		for filename in os.listdir(path):
			id = filename.split('.')[0]
			if result_tag_dict.has_key(id):
				print "Previous movie exist"
				continue
			if main_algorithm_control != 1 and id not in top_250_id_set:
				continue					
			if not keyword_hd.setReviewPath(path + '/' + filename): #Review Do Not Enough
				continue
			print id
			func,arg = method[main_algorithm_control]
			keywords = func(arg)
			result_tag_dict[id] = keywords
	f = open(method_file_list[main_algorithm_control],'w')
	f.write(json.dumps(result_tag_dict,ensure_ascii=False,sort_keys=True, indent=2))
	f.close()
