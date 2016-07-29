# -*- coding:utf-8 -*-
import requests
from HTMLParser import HTMLParser

class ZhihuClient(object):
    def __init__(self):
        headers={"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
                 "origin":"https://www.zhihu.com"}
        #create requests session
        self.session=requests.Session()
        self.session.headers.update(headers)

    def login(self,username,password):
        url='https://www.zhihu.com/login/phone_num'
        #access login page to get captcha
        r=self.session.get(url,verify=False)
        _xsrf=_get_xsrf(r.content)

       #post login request
        data={'phone_num':username,
              'password':password,
              }
     
        if _xsrf:
            data['_xsrf']=_xsrf
        headers={'referer':'https://www.zhihu.com/',
                 'host':'www.zhihu.com'}    
        r=self.session.post(url,data=data,headers=headers)

        #print(self.session.cookies.items())
        

    def edit_signature(self,signature):
        #access user's homepage
        #url='https://www.zhihu.com/people/%s/'%username
        #r=self.session.get(url,verify=False)
        #ck=_get_ck(r.content)

        #post requests to change signature
        url = 'https://www.zhihu.com/node/ProfileHeaderV2'
        headers={'referer':url,
                 'host':'www.douban.com',
                 'x-requested-with':'XMLHttpRequest'}
        data={'method':'save','params':'{"data":{"description":signature}}'}
        r=self.session.get(url,data=data,headers=headers)

def _attr(attrs,attrname):
    for attr in attrs:
        if attr[0]==attrname:
            return attr[1]
    return None

def _get_xsrf(content):

    class CaptchaParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self._xsrf=None  

        def handle_starttag(self,tag,attrs):
            if tag=='input' and _attr(attrs,'type')=='hidden' and _attr(attrs,'name')=='_xsrf':
                self._xsrf=_attr(attrs,'value')
                print self._xsrf
            #if tag=='img' and _attr(attrs,'id')=='captcha_image' and _attr(attrs,'class')=='captcha_image':
                #self.captcha_url=_attr(attrs,'src')
            
    p=CaptchaParser()
    p.feed(content)
    return p._xsrf

def _get_ck(content):

    class CKParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.ck=None
        def handle_starttag(self,tag,attrs):
            if tag=='input' and _attr(attrs,'type')=='hidden' and _attr(attrs,'name')=='ck':
                self.ck=_attr(attrs,'value')

    p=CKParser()
    p.feed(content)
    return p.ck


if __name__=='__main__':
    c=ZhihuClient()
    c.login('13588123739','xiaogang05095656')
    c.edit_signature('Python2016')
              
