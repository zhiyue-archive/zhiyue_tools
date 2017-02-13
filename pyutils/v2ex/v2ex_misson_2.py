#!/usr/bin/python
# -*- coding:utf-8 -*-
 
import re
import sys
import requests
 
reload(sys)
sys.setdefaultencoding('utf8')
 
def get_session():
    '''
    get requests session, which automatically handles cookies for us 
    '''
    v2ex_session = requests.Session()
    user_agent = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/32.0.1700.107 Chrome/32.0.1700.107 Safari/537.36"
 
    header = {'User-Agent': user_agent,
              'Host': 'www.v2ex.com',
              'Origin': 'http://www.v2ex.com',
              'Referer': 'http://www/v2ex.com/signin',
    }
    v2ex_session.headers.update(header)
    return v2ex_session
 
 
def main():
    
    # define urls will be used
    index_url = 'http://v2ex.com'
    sign_url = 'http://v2ex.com/signin'
    mission_url = 'http://v2ex.com/mission/daily'
 
    # fill in username and password here
    username = ''
    password = ''
 
    # find login needed value 'once', which is hidden in login form
    v2ex_session = get_session()
    v2ex_session.get(index_url)
    login = v2ex_session.get(sign_url)
    once = re.findall('value="(.*)" name="once"', login.content)[0]
    postdata = {
        'u': username,
        'p': password,
        'once': once,
        'next': '/'
    }
 
    # after login, go to mission page to find mission link
    v2ex_session.post(sign_url, data=postdata)
    mission_page = v2ex_session.get(mission_url)
    if "每日登录奖励已领取" in mission_page.text:
    	print "每日奖励已领取"
    	return
 
    # if mission is not done yet, get it
    mission = re.findall("onclick=.* = '(.*)'", mission_page.content)[0]
    mission = index_url + mission
 
    v2ex_session.get(mission)
 
if __name__ == "__main__":
	main()