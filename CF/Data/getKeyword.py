#-*-encoding:utf-8-*-
import os
import sys
import json
sys.path.append("../../Keyword/")
from keyword_extract import KeywordHandler
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#########Review tag should be regularized

keyword_handler = KeywordHandler(20)

movie_tag_dict = dict()

review_directory = "/home/wucanrui/Desktop/毕业论文/Crawler/长评"
for i in range(20,99):
	inner_directory = review_directory + '/' + str(i/10.0)
	for filename in os.listdir(inner_directory):
		movie_id = filename.split('.')[0]
		print movie_id
		filename = inner_directory+"/"+filename
		keyword_handler.setReviewPath(filename)
		movie_tag_dict[movie_id] = keyword_handler.normalTfIDF(0)

with open('Review_tag.json','w') as f:
	f.write(json.dumps(movie_tag_dict,ensure_ascii=False,sort_keys=True, indent=2))
