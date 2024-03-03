# import mechanize
import time
import http.cookiejar

#Dealing with Unicode encoding....
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')


# Set Cookie Jar so we can stay logged in...
# br.set_cookiejar(cookie_jar)


# 使用 time() 函数
start_time = time.time()

br = mechanize.Browser()
# br.set_handle_equiv(True)
# br.set_handle_redirect(True)
# br.set_handle_referer(True)
br.set_handle_robots(False)
# br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
# br.set_debug_http(True)
# br.set_debug_redirects(True)
# br.set_debug_responses(True)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open("https://www.baidu.com/")
br.select_form(nr = 0)
br.form['wd'] = 'python mechanize'
br.submit()
brr=br.response().read();
# print(brr)

end_time = time.time()

# 计算耗时
elapsed_time = end_time - start_time

print("耗时:", elapsed_time, "秒")