
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

with open('Review_tag.json') as f:
	contents = json.load(f)

for id in contents:
	contents[id] = contents[id][:3]

with open('tag.json','w') as f:
	f.write(json.dumps(contents,ensure_ascii=False,sort_keys=True, indent=2))
