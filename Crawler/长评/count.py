import json
import os

review_num = dict()
for i in range(21):
	review_num[i] = 0

for score in range(20,100):
	print score
	path = str(score/10.0)
	for filename in os.listdir(path):
		sentences = []
		f = open(path+"/"+filename)
		content = json.load(f)
		if len(content["data"]) >= 20:
			review_num[20] += 1
		else:
			review_num[len(content["data"])] += 1

print review_num
