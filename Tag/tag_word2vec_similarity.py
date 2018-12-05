#-*-encoding:utf-8-*-
import json
from gensim.models import Word2Vec
import sys
import os
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')



reviews_path = "../Crawler/长评/"
reviews_cut = []

def consineSimilarity(list1,list2):
	if len(list1) != len(list2):
		raise Exception("Wrong length")
	a,b,c = 0,0,0
	for i in range(len(list1)):
		a += list1[i]*list2[i]
		b += list1[i]*list1[i]
		c += list2[i]*list2[i]
	return a/(sqrt(b)*sqrt(c))

if __name__ == '__main__':
	model = None
	if os.path.exists("tag_similarity.model"):
		print "Model exists,Start Loading"
		model = Word2Vec.load("tag_similarity.model")
	else:
		for i in range(20,99):
			print i
			for filename in os.listdir(reviews_path+str(i/10.0)):
				filename = reviews_path+str(i/10.0)+"/"+filename
				with open(filename) as f:
					reviews = json.load(f)["data"]
					for review in reviews:
						reviews_cut.append(list(jieba.cut(review)))
		
		model = Word2Vec(reviews_cut, size=100, window=5, min_count=1, workers=4)
		model.save("tag_similarity.model")

	tag_list = []
	with open('allow_tag.txt') as f:
		for line in f.readlines():
			tag_list.append(line[:-1])
	tag_vector_dict = dict()
	tag_similar_dict = dict()
	for tag in tag_list:
		try:
			tag_vector_dict[tag] = model.wv[tag]
		except:
			continue

	print len(tag_vector_dict)
	for tag1 in tag_vector_dict:
		temp = dict()
		tag_similar_dict[tag1] = dict()
		for tag2 in tag_vector_dict:
			if tag1 == tag2:
				continue
			temp[tag2] = consineSimilarity(model.wv[tag1],model.wv[tag2])
		result = sorted(temp.items(),key = lambda item:item[1],reverse=True)
		for tag2,value in enumerate(result[:10]):
			tag_similar_dict[tag1][tag2] = value
	with open('similar_tag.json','w') as f:
		f.write(json.dumps(tag_similar_dict,ensure_ascii=False,sort_keys=True, indent=2))
		
