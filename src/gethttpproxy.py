
# -*- coding: utf-8 -*-# Project : 爬取代理IP并且测试可用IP# Tool : PyCharm

import requests
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
  }

# 提取网页源码
def getHtml(url):
  try:
    reponse = requests.get(url, headers=header)
    reponse.raise_for_status()
    reponse.encoding = reponse.apparent_encoding
    return reponse.text
  except:
    return "网页源码提取错误"


# 解析网页，提取IP
def getIp(html, list):
    try:
        soup = BeautifulSoup(html, "html.parser")
        tr = soup.find("tbody").find_all_next("tr")
        for ip in tr:
            # 提取IP
            td = ip.find_next("td").string
            td = str(td).replace(" ", "").replace("\n", "").replace("\t", "")
            # 提取端口号
            dk = ip.find_all_next("td")[1].string
            dk = str(dk).replace(" ", "").replace("\n", "").replace("\t", "")
            # 将IP和端口号进行连接
            ip = td + ":" + dk
            list.append(ip)  # 再进IP地址存放至指定列表中去
    except:
        print("获取IP失败")


# 测试出可用IP
def ip_text(list, valid_IP):
    try:
        url = "https://www.baidu.com//"
        for ip in list:
            try:
                rep = requests.get(url, proxies={'https': ip}, headers=header, timeout=0.5)
                if rep.status_code == 200:  # 如果放回的状态码是200，那么说明该IP地址可用
                    valid_IP.append(ip)
                    print("该代理IP有效：" + ip)
                else:
                    print("该代理IP无效：" + ip)
            except:
                print("该代理IP无效：" + ip)
    except:
        print("IP测试失败")


if __name__ == '__main__':
    valid_IP = []  # 有效IP地址
    for i in range(1, 9):  # 可自定义页数
        ip_list = []  # 存放所有爬取到的ip
        url = "https://www.89ip.cn/index_" + str(i) + ".html"
        print(url)
        html = getHtml(url)
        getIp(html, ip_list)
        ip_text(ip_list, valid_IP)

    print("=" * 30)
    print("测试完成，有效IP如下:")
    print("-" * 30)
    for a in valid_IP:
        print(a)
    print("=" * 30)
