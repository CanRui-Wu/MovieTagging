#-*-encoding:utf-8-*-
import telnetlib
import requests
import random
import os
import time
from bs4 import BeautifulSoup

real_dir = os.path.split(os.path.realpath(__file__))[0]
class ProxyHandler:
	lines = []
	def __init__(self):
		self.upDate()
		
	def check(self,url):
		headers = {
	    	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
		}
		proxies = {
			'http':"http://"+url,
			'https':"https://"+url
		}
		try:
			page = requests.get('https://www.baidu.com',headers=headers,proxies=proxies,timeout=3)
		except:
			return False
		else:
			return True
	def checkList(self,url_list,avail_list):
		for url in url_list:
			if self.check(url):
				print "successful," + url
				avail_list.append(url)

	def deleteFail(self,url):
		print url
		for i,line in enumerate(self.lines):
			if line[:-1] == url:
				del self.lines[i]
				print "delete " + line[:-1]
				break
		if len(self.lines) < 1:
			print "No enough proxies in pool,updating avail pool from internet now"
			self.upDateAvailList()
			#self.upDate()

	def getRandomProxy(self):
		random_index = random.randint(0,len(self.lines)-1)
		return self.lines[random_index][:-1]

	#Get new proxy list from mipu proxy api,and discard the useless proxy
	def upDateAvailList(self):
		proxy_pool_url = "https://proxyapi.mimvp.com/api/fetchsecret.php?orderid=860451920856143400&num=10&time_avail=10&http_type=3&result_fields=1,2,3"
		headers = {
    		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
		}
		while True:
			try:
				page = requests.get(proxy_pool_url,headers=headers,timeout=30)
				break
			except:
				time.sleep(20)
				continue
		bs = BeautifulSoup(page.text,"lxml")
		content = bs.find_all("p")[0].string
		url_list = [url.split(',')[0] for url in content.split('\n')]
		avail_list = []
		self.checkList(url_list,avail_list)
		self.lines= [i+'\n' for i in avail_list]
		f = open(real_dir+'/avail_proxy.txt','w')
		for url in avail_list:
			f.write(url)
			f.write('\n')

	def upDate(self):
		f = open(real_dir+"/avail_proxy.txt")
		self.lines = f.readlines()
		f.close()

if __name__ == '__main__':
	proxy_handler = ProxyHandler()
	proxy_handler.upDateAvailList()
	
