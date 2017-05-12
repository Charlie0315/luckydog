# -*- coding: utf-8 -*-
import sqlite3
import requests
import json
import time
import datetime
from selenium import webdriver
import re

class FacebookProcess(object):
    
    
    def __init__(self, email, password):
        self.login(email, password)
        self.fb_version = 'v2.9'
        self.fb_dtsg = self.driver.find_element_by_name("fb_dtsg").get_property("value")
        self.cookie = '; '.join(['{}={}'.format(item.get('name'), item.get('value'))for item in self.driver.get_cookies()])
        self.token = self.get_access_token()
        
    def login(self, email, password):
        self.driver = webdriver.Firefox()
        self.driver.get('https://zh-tw.facebook.com/login')
        time.sleep(3)
        self.driver.find_element_by_id("pass").clear()
        self.driver.find_element_by_id("pass").send_keys(password)
        self.driver.find_element_by_id("email").clear()
        self.driver.find_element_by_id("email").send_keys(email)
        self.driver.find_element_by_id("loginbutton").click()
        time.sleep(3)
    
    def get_access_token(self):
        headers = {
        'cookie':self.cookie
        }
        res = requests.get('https://developers.facebook.com/tools/explorer/', headers=headers)
        token = re.findall(r'\"accessToken\":\"([A-Za-z0-9_]*)\"', res.text)[0]
        return token
        
    def like_post(self, post_id):
        data2 = 'client_id=1494422643451:996525474&ft_ent_identifier={}&reaction_type=1&fb_dtsg={}'.format(post_id.split('_')[1], self.fb_dtsg)
        headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'referer':'https://www.facebook.com/',
        'cookie':self.cookie
        }

        requests.post('https://www.facebook.com/ufi/reaction/?dpr=1', data=data2, headers=headers)
        
    def like_post2(self, post_id):
        self.driver.get('https://www.facebook.com/{}'.format(post_id))
        time.sleep(5)
        try: self.driver.find_element_by_link_text(u"讚").click()
        except: self.driver.find_element_by_xpath(u"(//a[contains(text(),'讚')])[12]").click()
            
    def like_page(self, page_id):
        self.driver.get('https://www.facebook.com/{}'.format(page_id))
        time.sleep(5)
        self.driver.find_element_by_xpath("(//button[@value='1'])[2]").click()

    def share_post(self, link):
        attachment = {
        "link": link,
        "privacy": "{'value':'EVERYONE'}",
        }
        requests.post('https://graph.facebook.com/{}/me/feed?access_token={}'.format(self.fb_version, self.token), data=attachment)

    def fblink_to_post_id(self, fb_link):
        post_id = fb_link.split('/')[-1]
        page_name = fb_link.split('/')[3]
        res = requests.get('https://graph.facebook.com/{}/{}?access_token={}'.format(self.fb_version, page_name, self.token))
        page_id = json.loads(res.text)['id']
        
        return page_id + '_' + post_id
    
    def post_comment(self, post_id, message, tags):
        tags = ''.join(["@[{}:{}]".format(key, value) for key, value in tags.items()])
        data2 = """ft_ent_identifier={}&comment_text={}{}
        &source=21&client_id=1493913966456:1963482973&fb_dtsg={}""".format(post_id.split('_')[1], tags, message.encode('utf8'), self.fb_dtsg)
        headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36', 
        'referer':'https://www.facebook.com/',
        'cookie':self.cookie
        }
        
        requests.post("https://www.facebook.com/ufi/add/comment/?dpr=1", data=data2, headers=headers)