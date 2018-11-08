#-*-encoding:utf-8-*-
import json
import time
import urllib
import requests
import os
from bs4 import BeautifulSoup
import sys
import loginModel.login as login
reload(sys)
sys.setdefaultencoding('utf-8')

def getContent(url,Session):
	headers = {
    	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
	}
	proxies = {
		"http":"http://1ff474e33903:5c2aa9e37b@111.230.10.75:12056",
		"https":"https://1ff474e33903:5c2aa9e37b@111.230.10.75:12056"
	}
	page = Session.get(url,headers=headers,proxies=proxies,timeout=5)
	#page = Session.get(url,headers=headers,timeout=5)
	bs = BeautifulSoup(page.text,"lxml")
	all_movie = bs.find_all("div",attrs={"class":"article"})[0].find_all("table")
	result = []
	for movie in all_movie[1:]:
		link = movie.find_all("a",attrs={"class":"nbg"})[0]["href"].split('/')[-2]
		result.append(link)
	return result

douban_tag = []


with open('douban_tag.txt') as f:
	for line in f.readlines():
		douban_tag.append(line[:-1])
douban_tag.reverse()


tag_movie_dict = dict()
if os.path.exists('tag_search_complete.json'):
	f = open('tag_search_complete.json')
	tag_movie_dict = json.load(f)
	f.close()


url_head = "https://movie.douban.com/tag/"
url_tail1 = "?start="
url_tail2 = "&type=T"
# cookie_hd = login.CookieHandler()
# cookie_hd.updateCookie()
# cookie = cookie_hd.getCookieDict()
# cookie = requests.utils.cookiejar_from_dict(cookie)
Session = requests.session()
# Session.cookies = cookie


for tag in douban_tag:
	result = []
	count = 0
	if tag_movie_dict.has_key(tag.decode('utf-8')):
		continue
	print "正在处理" + tag
	while True:
		try:
			time.sleep(1)
			temp = getContent(url_head+urllib.quote(tag)+url_tail1+str(count*20)+url_tail2,Session)
			result.extend(temp)
			if len(temp) != 0:
				count += 1
			else:
				break
			print "ok"
		except:
			print "error"
			time.sleep(2)
			continue
	tag_movie_dict[tag.decode('utf-8')] = result
	print tag + "一共有" + str(len(result)) + "部电影"
	f = open('tag_search_complete.json','w')
	f.write(json.dumps(tag_movie_dict,ensure_ascii=False,sort_keys=True, indent=2))
	f.close()




