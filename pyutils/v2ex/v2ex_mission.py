#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as pq
 
 
class V2User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.is_loggin = False
 
    def login(self):
        if self.is_loggin:
            return
        signin_url = "http://www.v2ex.com/signin"
        headers = {"Referer": 'http://www.v2ex.com'}
        get_r = self.session.get(signin_url, headers=headers, verify=False)
        d = pq(get_r.text)
        once = d("input[name='once']").val()
        payload = {
            "u": self.username,
            "p": self.password,
            "once": once,
            "next": "/",
        }
        headers = {"Referer": signin_url}
        r = self.session.post(signin_url, data=payload,
                              headers=headers, verify=False)
        if r.history:
            self.is_loggin = True
            print 'logged in'
 
    def daily_mission(self):
        if not self.is_loggin:
            self.login()
        mission_url = "http://www.v2ex.com/mission/daily"
        redeem_url = "http://www.v2ex.com/mission/daily/redeem"
        headers = {"Referer": "http://www.v2ex.com"}
        r = self.session.get(mission_url, headers=headers, verify=False)
        # get once code
        i = r.text.index('redeem?once=')
        once = r.text[i+12:i+22]
        i = once.index("'")
        once = once[0:i]
        payload = {"once": once}
        headers = {"Referer": mission_url}
        self.session.get(redeem_url, headers=headers,
                         params=payload, verify=False)
        print 'done'
 
 
def test():
    v2user = V2User('yourusername', 'yourpassword')
    v2user.daily_mission()
 
if __name__ == '__main__':
    test()