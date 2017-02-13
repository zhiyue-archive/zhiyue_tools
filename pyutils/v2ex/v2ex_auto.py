#! /usr/bin/env python
# -*- coding: utf-8 -*-
 
import requests
from bs4 import BeautifulSoup
 
signin_url = "http://www.v2ex.com/signin"
award_url = "http://www.v2ex.com/mission/daily"
main_url = "http://www.v2ex.com"
 
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) \
AppleWebKit/537.31 (KHTML, like Gecko) \
Chrome/26.0.1410.65 Safari/537.31"
post_headers = {"User-Agent": user_agent,
                "Referer": "http://www.v2ex.com/signin"
                }
headers = {"User-Agent": user_agent}
v2ex_session = requests.Session()
 
 
def get_logininfo(usr_name, passwd):
    v2ex_main_req = v2ex_session.get(signin_url, headers=headers)
    v2ex_main_tag = BeautifulSoup(v2ex_main_req.content)
 
    form_tag = v2ex_main_tag.find('form',
                                  attrs={"method": "post", "action": "/signin"}
                                  )
    input_once_tag = form_tag.find('input', attrs={"name": "once"})
    input_once_value = input_once_tag.attrs["value"]
 
    logininfo = {"next": "/",
                 "u": usr_name,
                 "p": passwd,
                 "once": input_once_value,
                 "next": "/"
                 }
    return logininfo
 
 
def get_award(usr_name, passwd):
    logininfo = get_logininfo(usr_name, passwd)
    v2ex_session.post(signin_url,
                      data=logininfo,
                      headers=post_headers,
                      )
 
    # get the user's money if login successfully
    main_req = v2ex_session.get(main_url, headers=headers)
    if "auth" not in main_req.cookies:
        print "login fails..."
        return
 
    main_soup = BeautifulSoup(main_req.content)
    money_tag = main_soup.find(href="/balance", class_="balance_area")
    if not money_tag:
        print "Get money fails..."
        return
 
    money = money_tag.contents[0] + money_tag.contents[2]
    print "Your money: ", money
 
    award_tag = main_soup.find(href="/mission/daily")
    if not award_tag:
        print "You haved got the award."
        return
 
    # get the award
    get_award_req = v2ex_session.get(award_url, headers=headers)
    get_award_soup = BeautifulSoup(get_award_req.content)
    button_tag = get_award_soup.find('input', attrs={"type": "button"})
    click_href = button_tag.attrs["onclick"]
    first_dot_index = click_href.find("'")
    last_dot_index = click_href.find("'", first_dot_index + 1)
    click_url = main_url + click_href[first_dot_index+1:last_dot_index]
 
    award_req = v2ex_session.get(click_url, headers=headers)
    award_soup = BeautifulSoup(award_req.content)
    result_tag = award_soup.find('div', class_="message")
    print result_tag.string
 
if __name__ == "__main__":
    usrname = raw_input("username: ")
    passwd = raw_input("password: ")
    get_award(usrname, passwd)