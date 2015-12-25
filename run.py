#!/bin/env python
#encoding=utf-8
# Author: Aaron Shao - shao.dut#gmail
# Last modified: 2015-12-24 18:12
# Filename: run.py
# Description: 

import sys,mechanize
import cookielib
import random
import re
import time

#Browser
br = mechanize.Browser()
cj = cookielib.LWPCookieJar()

#options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
#br.set_cookiejar(cj)

#Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

#debugging?
br.set_debug_http(False)
br.set_debug_redirects(False)
br.set_debug_responses(False)

#User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

#Login
home_url = "http://t66y.com/index.php"
try:
    r = br.open(home_url)
    br.select_form(nr = 0)
    br['pwuser'] = 'namen'
    br['pwpwd'] = 'liangzhishanyang'
    time.sleep(2)
    resp = br.submit()
except Exception as e:
    print "Login Failed, ", e
    sys.exit(-1)


visited_post_set = set([])

commit_str_list = [
        u'谢谢分享',
        u'感谢分享',
        u'感谢分享！！！',
        u'好人一生平安',
        u'谢谢分享，辛苦了',
        u'楼主辛苦了',
        ]

#Loop Forever
while True:
    html = br.response().read().replace('"','\n')
    post_ids = re.findall(r'read\.php\?tid=\d+', html)
    post_ids = list(set(post_ids) - visited_post_set)

    if len(post_ids) >= 1:

        post_id = random.choice(post_ids)
        post_url = "http://t66y.com/" + post_id
        time.sleep(2)
        try:
            r = br.open(post_url) 
            br.select_form(nr = 0) 
            content = random.choice(commit_str_list)
            br['atc_content'] = content.encode('gbk') 
            time.sleep(2)
            resp = br.submit() 
        except Exception as e:
            print "reply error, ", e
            visited_post_set.add(post_id)
            time.sleep(10)
            continue

        visited_post_set.add(post_id)
        print "replyed on ", post_url
    else:
        print "no new post"

    #a ha!
    time.sleep(1024)
    try:
        r = br.open(home_url)
    except Exception as e:
        print "open home error, ", e
        sys.exit(-1)



