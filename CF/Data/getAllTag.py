#-*-encoding:utf-8-*-
#这个文件简单的用于统计目前使用的标签

import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

source_file_path = "/home/wucanrui/Desktop/毕业论文/Crawler/all_tag_search.json"




tag_set = set()



with open(source_file_path) as f:
	contents = json.load(f)
	for movie_id in contents:
		for tag in contents[movie_id]:
			tag_set.add(tag)

with open("allow_tag.txt",'w') as f:
	for tag in tag_set:
		f.write(tag)
		f.write('\n')