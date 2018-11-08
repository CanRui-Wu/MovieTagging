#-*-encoding:utf-8-*-
import telnetlib
import os
import requests
import json
import sys
import time
import proxy.proxy_utils as proxy_utils
import loginModel.login as login
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')
all_data = dict()
all_data["data"] = []
proxy_handler = proxy_utils.ProxyHandler()
def getContent(url,Session):
	headers = {
    	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
	}
	page = Session.get(url,headers=headers,timeout=10)
	bs = BeautifulSoup(page.text,"lxml")
	all_content = bs.find_all("p")[0].string
	current_data = json.loads(all_content)
	if current_data.has_key("code"):
		print current_data["code"]
		if current_data["code"] == 112:
			return 0
		else:
			return 1
	all_data["data"].append(current_data)
	return 1

def getMovieDetail(input_json,Session):
	f = open("电影列表/"+input_json)
	all_movie = json.load(f)["data"]
	all_data["data"] = []
	for movie in all_movie:
		count = 0
		while count < 20:
			try:
				time.sleep(10)
				if getContent("http://api.douban.com/v2/movie/subject/"+movie["id"],Session) == 1:
					print "succefully,go next movie"
					break
				else:
					print movie["id"]+" " + str(count)+" exceed speed limited"
					time.sleep(600)
					count += 1
					continue
			except:
				print movie["id"]+" " + str(count)+" failed"
				count += 1
	json_file = open("电影详细属性/"+input_json,'w')
	json_file.write(json.dumps(all_data,ensure_ascii=False,sort_keys=True, indent=2))
	json_file.close()


if __name__ == "__main__":
	cookie_hd = login.CookieHandler()
	cookie_hd.updateCookie()
	cookie = cookie_hd.getCookieDict()
	Session = requests.session()
	cookie = requests.utils.cookiejar_from_dict(cookie)
	Session.cookies = cookie
	for ten_score in range(80,85):
		score = ten_score/10.0
		if os.path.exists("电影详细属性/"+str(score)+".json"):
			print str(score)+" exists,go next score"
			continue
		print "**** Now starting handle" + str(score) + " movie ****"
		getMovieDetail(str(score)+".json",Session)
