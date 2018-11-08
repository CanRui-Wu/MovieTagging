import requests
import loginModel.login as login
from bs4 import BeautifulSoup

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
}
url_head = "https://movie.douban.com/top250?start="
url_tail = "&filter="

top_250_id = []
cookie_hd = login.CookieHandler()
cookie_hd.updateCookie()
cookie = cookie_hd.getCookieDict()
Session = requests.session()
cookie = requests.utils.cookiejar_from_dict(cookie)
Session.cookies = cookie
for i in range(10):
	url = url_head+str(i*25)+url_tail
	headers = {
    	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
	}
	page = Session.get(url,headers=headers,timeout=10)
	bs = BeautifulSoup(page.text,"lxml")
	all_content = bs.find_all("ol",attrs={"class":"grid_view"})
	for li in all_content[0].find_all("li"):
		link = li.find_all("a")[0]
		top_250_id.append(link["href"].split('/')[-2])

f = open('top250.txt','w')
for id in top_250_id:
	f.write(id)
	f.write('\n')
f.close()
