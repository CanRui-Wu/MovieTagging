#-*-encoding:utf-8-*-
import requests
import pickle
from os import remove
from PIL import Image
from bs4 import BeautifulSoup

class CookieHandler:
    url= 'https://www.douban.com'
    login_url = 'https://www.douban.com/login'
    headers = {'Host': 'www.douban.com',
               'Referer': 'https://www.douban.com/',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
               'Accept-Encoding': 'gzip, deflate, br'}

    def getCaptcha(self):
        req = requests.get(self.login_url)
        page = BeautifulSoup(req.text,'lxml')
        try:
            img_src = page.find('img',id='captcha_image').get('src')
        except:
            return 'NULL','NULL'
        img = requests.get(img_src)
        if img.status_code == 200:
            with open('captcha.jpg','wb') as f:
                f.write(img.content)
        image = Image.open('captcha.jpg')
        image.show()
        captcha = raw_input('Please input the captcha:')
        remove('captcha.jpg')
        captcha_id = img_src[img_src.find('=')+1:]
        captcha_id = captcha_id[:captcha_id.find('&')]
        return captcha,captcha_id

    def updateCookie(self):
        data={
            'source':None,
            'remember':'on',
            'form_email':'434858383@qq.com',
            'form_password':'xxxx'
        }
        captcha, captcha_id = self.getCaptcha()
        if captcha != 'NULL':
            data['captcha-solution'] = captcha
            data['captcha-id'] = captcha_id
        Session = requests.session()
        page_login = Session.post(self.login_url,data=data,headers=self.headers)
        page_login_bf = BeautifulSoup(page_login.text,'lxml')
        with open('cookie','wb') as f:
            pickle.dump(Session.cookies,f)

    def getCookieDict(self):
        Session = requests.session()
        with open('cookie', 'rb') as f:
            Session.cookies = pickle.load(f)
        print Session.cookies
        print Session.cookies.get_dict()
        return Session.cookies.get_dict()


if __name__ == '__main__':
    cookie_hd = CookieHandler()
    cookie_hd.getCookieDict()
