#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mechanicalsoup


#appl = yf.Ticker("AAPL") 

# 取得したデータを確認します。

# ソフトバンクグループの情報を取得（Tは東証を表す）
#ticker_info = yf.Ticker("9984.T")

# 会社概要(info)を出力
#ticker_info.info



#print(appl.info);
# br = mechanize.Browser()
# br.open("http://www.cnblogs.com/baby123/p/8078508.html")
# print(br.title())

# request2 = mechanize.Request("https://news.cnblogs.com/")
# response2 = mechanize.urlopen(request2)
# print(response2.geturl())
# print(response2.info())


# browser = mechanicalsoup.Browser()
# br = mechanicalsoup.StatefulBrowser()
# br.set_handle_equiv(True)
# br.set_handle_redirect(True)
# br.set_handle_referer(True)
# br.set_handle_robots(False)
# # br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
# br.set_debug_http(True)
# br.set_debug_redirects(True)
# br.set_debug_responses(True)
# br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
# br.open("https://www.baidu.com/")
# br.select_form(nr = 0)
# br.form['wd'] = 'python mechanize'
# br.submit()
# brr=br.response().read();
# print(brr)




# Connect to Qwant
browser = mechanicalsoup.StatefulBrowser(user_agent='Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')
browser.open("https://www.baidu.com/")

# Fill-in the search form
# browser.select_form('#kw')
# browser.form['wd'] = 'python mechanize'
# browser.submit()
import time

# 使用 time() 函数
start_time = time.time()

form = browser.select_form('form')
form["wd"] = "python mechanize"
browser.submit_selected()

page = browser.get_current_page()
# results = page.find_all('div', {'class': 'result'})

# print(page)
# 执行需要计时的时间段

end_time = time.time()

# 计算耗时
elapsed_time = end_time - start_time

print("耗时:", elapsed_time, "秒")