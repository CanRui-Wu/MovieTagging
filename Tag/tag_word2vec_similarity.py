#-*-encoding:utf-8-*-
import json
from gensim.models import Word2Vec
import sys
import os
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')

reviews_path = "../Crawler/长评/"




def reviewGenerator():
	for i in range(20,99):
		print i
		for filename in os.listdir(reviews_path+str(i/10.0)):
			filename = reviews_path+str(i/10.0)+"/"+filename
			with open(filename) as f:
				reviews = json.load(f)["data"]
				for review in reviews:
					yield list(jieba.cut(review))

model = Word2Vec(reviewGenerator(), size=100, window=5, min_count=1, workers=4)
model.save("tag_similarity.model")