
# -*- coding: utf-8 -*-# Project : 爬取代理IP并且测试可用IP# Tool : PyCharm

from bs4 import BeautifulSoup
import requests
import socks

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
  }

proxies = [
"http://58.234.116.100:80",
"http://91.202.230.219:8080",
"http://110.141.192.123:80",
"http://51.79.40.227:80",
"http://95.138.193.63:80",
"http://144.91.97.235:80",
"http://149.156.33.134:80",
"http://14.7.183.127:80",
"http://80.39.228.110:80",
]



# 测试出可用IP
def check_proxy(valid_IP):
  url = "http://icanhazip.com/"
  for proxip in proxies:
#     // useragents[random.randint(0, len(useragents)-1)]
    try:
      rep = requests.get(url, proxies={'http': proxip} , headers=header, timeout=5)
      # 利用访问http://icanhazip.com/返回的IP进行测试
      if rep.status_code == 200 and rep.text.strip() in proxip:  # 如果放回的状态码是200，那么说明该IP地址可用
        valid_IP.append(proxip)
        print("该代理IP有效：" + proxip)
    except Exception as ex:
      print(ex)
      print("该代理IP无效：" + proxip)


if __name__ == '__main__':
    valid_IP = []  # 有效IP地址
    check_proxy(valid_IP)

    print("=" * 30)
    print("测试完成，有效IP如下:")
    print("-" * 30)
    for a in valid_IP:
      print("\""+ a +"\",")
    print("=" * 30)
