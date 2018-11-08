#-*-encoding:utf-8-*-
import telnetlib
import requests
import json
import sys
import time
import os
import proxy.proxy_utils as proxy_utils
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import loginModel.login as login
reload(sys)
sys.setdefaultencoding('utf-8')

all_data = dict()
all_data["data"] = []
proxy_handler = proxy_utils.ProxyHandler()

def getContent(url,browser):
	browser.set_page_load_timeout(30)
	browser.set_script_timeout(30)
	ok = 1
	try:
		browser.get(url)
	except:
		print "Try continue"
		ok = 0
	for button in browser.find_elements_by_link_text("展开"):
		try:
			button.send_keys(Keys.ENTER)
		except:
			continue
	time.sleep(3)
	bs = BeautifulSoup(browser.page_source,"lxml")
	if len(bs.find_all("a")) == 1:
		return 2
	all_content = bs.find_all("div",attrs={"class":"review-content"})
	print len(all_content)
	if len(all_content) == 0 and ok == 1:
		return 0
	for content in all_content:
		all_data["data"].append(content.getText(separator='\n'))
	return 1

def getMovieDetail(input_json,browser):
	f = open("电影列表/"+input_json)
	all_movie = json.load(f)["data"]
	#按评分划分文件夹，一部电影的评论对应一个json文件
	review_dir = input_json.split('.')[0]+'.'+input_json.split('.')[1]
	for movie in all_movie:
		if os.path.exists("长评/"+review_dir+"/"+movie["id"]+".json"):
			print movie["id"]+" exist,continue"
			continue
		all_data["data"] = []
		for i in range(0,1000):
			count = 0
			ok = 0
			while count < 20:
				time.sleep(1)
				try:
					value = getContent("https://movie.douban.com/subject/"+movie["id"]+"/reviews?start="+str(i*20),browser)
					if value == 0:
						ok = 1
						break
					elif value == 1:
						break
					else:
						print movie["id"]+" " + str(count)+" failed,speed limited exceed"
						time.sleep(1200)
						count += 1 
				except:
					print movie["id"]+" " + str(count)+" failed"
					count += 1
			if ok == 1:
				break
		#路径为长评/"评分"/"电影id".json			
		json_file = open("长评/"+review_dir+"/"+movie["id"]+".json",'w')
		json_file.write(json.dumps(all_data,ensure_ascii=False,sort_keys=True, indent=2))
		json_file.close()

if __name__ == "__main__":
	cookie_hd = login.CookieHandler()
	cookie_hd.updateCookie()
	cookie = cookie_hd.getCookieDict()
	browser = webdriver.Firefox()
	browser.get("https://www.douban.com")
	time.sleep(2)
	browser.delete_all_cookies()
	for key, value in cookie.items():
		browser.add_cookie({"domain": ".douban.com", "name": key, "value": value, 'path': '/', 'expries': None})
	for ten_score in range(21,100):
		score = ten_score/10.0
		print "**** Now starting handle" + str(score) + " movie ****"
		getMovieDetail(str(score)+".json",browser)
	
