#!/usr/bin/env python                                                                                                                                 
# -*- coding: utf-8 -*-
 
import sys, requests, re
from bs4 import BeautifulSoup
reload(sys)
 
sys.setdefaultencoding("utf-8")
 
 
class V2EX:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._s = requests.Session()
        self._login_url = "https://www.v2ex.com/signin"
        self._daily_url = "https://www.v2ex.com/mission/daily"
        self._redeem_url = "https://www.v2ex.com/mission/daily/redeem?once="
 
    def login(self):
        """
        登陆V2EX
        """
        self._headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0",
            "Host": "v2ex.com",
            "Origin": "http://v2ex.com",
            "Referer": "http://www.v2ex.com/signin"
        }
        login_page = self._s.get(self._login_url, headers=self._headers, verify=False).text
        soup = BeautifulSoup(login_page)
        once_value = soup.find(attrs={"name": "once", "type": "hidden"})["value"]
        self._post_data = {
            "next": "/",
            "u": self._username,
            "p": self._password,
            "once": once_value
        }
        r = self._s.post(self._login_url, data=self._post_data, headers=self._headers, verify=False)
        page = r.text
        soup = BeautifulSoup(page)
        if soup.find(class_="problem"):
            raise ValueError("用户名或密码错误!")
     
    def daily(self):
        """
        领取每日奖励
        """
        r = self._s.get(self._daily_url, headers=self._headers, verify=False)
        soup = BeautifulSoup(r.text)
        redeem = soup.find(class_="super normal button")
        redeem_href = redeem["onclick"]
        result = re.search(r"\d+", redeem_href)
        if result is None:
            print("每日登录奖励已领取")
            return
        once = result.group(0)
        redeem_url = self._redeem_url + once
        self._s.get(redeem_url, headers=self._headers, verify=False)
     
if __name__ == "__main__":
    username = "xxx@gmail.com"
    password = "xxxxx" 
    v2ex = V2EX(username, password)
    v2ex.login()
    v2ex.daily()