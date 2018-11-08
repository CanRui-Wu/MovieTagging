import json
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

f = open('movie_tag.json')
tag_dict = json.load(f)
real_tag_dict = dict()

for each in tag_dict:
	for tag in tag_dict[each]:
		if real_tag_dict.has_key(tag):
			real_tag_dict[tag] += 1
		else:
			real_tag_dict[tag] = 1

f = open('douban_tag.txt','w')
real_tag_dict = sorted(real_tag_dict.items(),key=lambda x:x[1],reverse=True)
for tag,value in real_tag_dict:
	if len(tag) != 2 or value == 1 or re.search('^[a-zA-Z0-9]+$', tag):
		continue
	f.write(tag)
	f.write('\n')
f.close()

