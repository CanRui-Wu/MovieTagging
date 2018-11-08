#-*-coding:utf-8-*-
import telnetlib
import requests
import json
import sys
import time
import proxy.proxy_utils as proxy_utils
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')

all_data = dict()
all_data["data"] = []
def getContent(url,proxy):
	headers = {
    	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
	}
	
	proxies = { 
		"http": "http://"+proxy,  
		"https": "https://"+proxy,  
	}
	page = requests.get(url,headers=headers,timeout=5,proxies=proxies)
	bs = BeautifulSoup(page.text,"lxml")
	all_content = bs.find_all("p")[0].string
	current_data = json.loads(all_content)
	if len(current_data["data"]) == 0:
		return 1 
	all_data["data"].extend(current_data["data"])
	return 0

url_head = "https://movie.douban.com/j/new_search_subjects?sort=T&range="
url_tail = "&tags=%E7%94%B5%E5%BD%B1&start="

proxy_handler = proxy_utils.ProxyHandler()
for ten_score in range(84,100):
	score = ten_score/10.0
	for i in range(0,10000):
		print score,i
		url = url_head + str(score)+","+str(score)+url_tail+str(20*i)
		count = 1
		ok = 0
		while count < 20:
			try:
				proxy = proxy_handler.getRandomProxy()
				if getContent(url,proxy) == 1:
					json_file = open("电影列表/"+str(score)+'.json','w')
					json_file.write(json.dumps(all_data,ensure_ascii=False,sort_keys=True, indent=2))
					json_file.close()
					all_data["data"] = []
					ok = 1
					break
				else:
					break
			except:
				print str(score)+","+str(i) + ","+ str(count) +" is failed"
				proxy_handler.deleteFail(proxy)
				count += 1
		if ok == 1:
			break


