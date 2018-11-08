#-*- encoding:utf-8 -*-
import os
import requests
import json
import time
import loginModel.login as login
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getContent(url,Session):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
	}
	proxies = { 
		"http": "http://120.192.179.121:53281",  
		"https": "https://120.192.179.121:53281",  
	}
	page = Session.get(url,headers=headers,timeout=10)
	bs = BeautifulSoup(page.text,"lxml")
	all_content = bs.find_all("div",attrs={"class":"tags-body"})
	result = []
	for content in all_content[0].find_all("a"):
		result.append(content.getText())
	return result

def getMovieTag(movie_tag_dict,input_json,Session):
	f = open("电影列表/"+input_json)
	all_movie = json.load(f)["data"]
	wrong_list = []
	num = 0
	for movie in all_movie:
		count = 0
		if movie_tag_dict.has_key(movie["id"]):
			print movie["id"]+" exist,continue"
			continue
		num += 1
		
		if num % 10 == 0:
			print "Succefully new 10 movie,Load again"
			f = open('movie_tag.json','w')
			f.write(json.dumps(movie_tag_dict,ensure_ascii=False,sort_keys=True, indent=2))
			f.close()
		while count < 2:
			try:
				time.sleep(1)
				result = getContent("https://movie.douban.com/subject/"+movie["id"]+"/?from=showing",Session)
				if len(result) == 0:
					wrong_list.append(movie["id"])
				movie_tag_dict[movie["id"]] = result
				print "sucessfully"
				break
			except:
				print movie["id"]+" " + str(count)+" failed"
				time.sleep(1)
				count += 1
				continue

if __name__ == "__main__":
	# cookie_hd = login.CookieHandler()
	# cookie_hd.updateCookie()
	# cookie = cookie_hd.getCookieDict()
	Session = requests.session()
	# cookie = requests.utils.cookiejar_from_dict(cookie)
	# Session.cookies = cookie
	movie_tag_dict = dict()
	if os.path.exists('movie_tag.json'):
		print "Loading previous movie tag"
		f = open('movie_tag.json')
		movie_tag_dict = json.load(f)
		f.close()
	
	for ten_score in range(20,100):
		score = ten_score/10.0
		print "Now starting building tag from " + str(score) + " movie"
		getMovieTag(movie_tag_dict,str(score)+".json",Session)
		f = open('movie_tag.json','w')
		f.write(json.dumps(movie_tag_dict,ensure_ascii=False,sort_keys=True, indent=2))
		f.close()
