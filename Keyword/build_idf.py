#-*-encoding:utf-8-*-
import os
import json
import math
import random
import jieba
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

jieba.enable_parallel(4)

class IDFHandler:
	all_path = "../Crawler/长评/"
	all_word = dict()
	file_count = 0

	def __init__(self,mode):
		if mode == 0:
			for score in range(20,100):
				print score
				path = self.all_path+str(score/10.0)
				for filename in os.listdir(path):
					sentences = []
					f = open(path+"/"+filename)
					content = json.load(f)
					self.file_count += 1
					for each in content["data"]:
						each = each.replace("\n",' ')
						sentences.append(jieba.cut(each))
					temp = set()
					for sentence in sentences:
						for word in sentence:
							temp.add(word)
					for word in temp:
						if self.all_word.has_key(word):
							self.all_word[word] += 1
						else:
							self.all_word[word] = 1		


	def outputIDF(self,filename,type):
		f = open(filename, 'w')
		all_word = sorted(self.all_word.items(), key=lambda x: x[1], reverse=True)
		if type == 0:
			for word in all_word:
				if word[1] == 0:
					value = 0
				else:
					value = math.log(float(self.file_count)/ word[1])
				f.write(word[0])
				f.write(" ")
				f.write(str(value))
				f.write('\n')
		elif type == 1:
			print "Output Document number of the word"
			for word in all_word:
				f.write(word[0])
				f.write(" ")
				f.write(str(word[1]))
				f.write('\n')
		f.close()



if __name__ == '__main__':
	print "Start Cutting"
	IDF_hd = IDFHandler(0)
	print "Start OutPut"
	IDF_hd.outputIDF('special.txt',1)
