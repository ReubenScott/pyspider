#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import time
import random
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup, SoupStrainer

from Words import Words
from Words import ExcelHandler

# 配置请求头
headers = {
#   'User-Agent': 'Mozilla /5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,application/json,image/webp,image/apng ,*/*;q=0.8,application/signed-exchange;v=b3',
  'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
  'Accept-Encoding': 'gzip, deflate, br',
  'Content-Type': 'application/json;charset=utf-8',
#   'Content-Type': 'text/html; charset=utf-8',
  'Connection': 'close'
}


#模擬header的user-agent字段，返回一個隨機的user-agent字典類型的鍵值對
useragents = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',  
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36',
  'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
  'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
  'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.51',
  'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'
]


cookies = [
  'HJ_UID=1d97c1e3-4982-851d-e2fb-9688a9cf8765; TRACKSITEMAP=3%2C6%2C20%2C23; _REF=https%3A%2F%2Fdict.hjenglish.com%2Fjp%2Fjc%2F%25E8%25B2%25B4%25E6%2596%25B9; _REG=dict.hjenglish.com%7C%7Cxiaodi_site%7Cdomain; _SREF_3=https%3A%2F%2Fdict.hjenglish.com%2Fjp%2Fjc%2F%E8%B2%B4%E6%96%B9; _SREG_3=dict.hjenglish.com%7C%7Cxiaodi_site%7Cdomain; _SREF_20=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DhuEIcpnuOcb6ULzhdTnwE8xiX4uRF1EAwlFc8cPh8rszH-a6knkQEEWAd0HYEnmT%26wd%3D%26eqid%3Df653c792000568c5000000056072c5e8; _SREG_20=www.baidu.com%7C%7Csearch%7Cdomain; _UZT_USER_SET_106_0_DEFAULT=2|6ed2e0a3900e22cb93d3dd68d679fad2; HJ_SID=djz0xw-d350-411a-be29-4bbf008627f8; HJ_SSID_3=djz0xw-935d-439d-be26-7ea49f256106; HJ_CST=0; HJ_CSST_3=1; acw_tc=2f624a2416189375318547181e14f93a3a5e54a9bf667711cfa1f39838005a',
  'HJ_UID=61fb377b-88ee-a3a1-8058-718ab5f6097d; TRACKSITEMAP=3%2C20%2C23; _REF=https%3A%2F%2Fdict.hjenglish.com%2Fjp%2Fjc%2F%E3%81%82%E3%81%A1%E3%82%89; _REG=direct%7C%7Cdirect%7Cdirect; _SREF_3=; _SREG_3=direct%7C%7Cdirect%7Cdirect; _SREF_20=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DKCJVBw943ECLx9-ap81lRDx4DJ2wdr4MMK9-HY1KCPuYYw6vkVwt1oeBc50rSX41%26wd%3D%26eqid%3Dec26d1f80004eeeb00000004607d1807; _SREG_20=www.baidu.com%7C%7Csearch%7Cdomain; Hm_lvt_d4f3d19993ee3fa579a64f42d860c2a7=1617957780,1618021323,1618294620,1618810892; _UZT_USER_SET_106_0_DEFAULT=2|6ed2e0a3900e22cb93d3dd68d679fad2; Hm_lpvt_d4f3d19993ee3fa579a64f42d860c2a7=1618810892; HJ_SID=oxl2bb-51af-4dfc-bf89-17bbfbdd60b2; HJ_SSID_3=oxl2bb-7b2e-4483-8bee-ee21f321ccb5; HJ_CST=0; HJ_CSST_3=1; acw_tc=707c9f9d16189714475066449e01f4914d4d6a1dfe79bfac97268fb6681cd4',
  'HJ_UID=61fb377b-88ee-a3a1-8058-718ab5f6097d; TRACKSITEMAP=3%2C20%2C23; _REF=https%3A%2F%2Fdict.hjenglish.com%2Fjp%2Fjc%2F%25E7%25BE%258A%25E6%25AF%259B; _REG=dict.hjenglish.com%7C%7Cxiaodi_site%7Cdomain; _SREF_3=https%3A%2F%2Fdict.hjenglish.com%2Fjp%2Fjc%2F%E7%BE%8A%E6%AF%9B; _SREG_3=dict.hjenglish.com%7C%7Cxiaodi_site%7Cdomain; _SREF_20=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DKCJVBw943ECLx9-ap81lRDx4DJ2wdr4MMK9-HY1KCPuYYw6vkVwt1oeBc50rSX41%26wd%3D%26eqid%3Dec26d1f80004eeeb00000004607d1807; _SREG_20=www.baidu.com%7C%7Csearch%7Cdomain; Hm_lvt_d4f3d19993ee3fa579a64f42d860c2a7=1617957780,1618021323,1618294620,1618810892; _UZT_USER_SET_106_0_DEFAULT=2|6ed2e0a3900e22cb93d3dd68d679fad2; Hm_lpvt_d4f3d19993ee3fa579a64f42d860c2a7=1618810892; acw_tc=2f624a4816189053457392237e0df8c605cf50e3a5b2d389c20027d1f163b1; HJ_SID=ra4zlx-1e1f-4399-b195-c4b0dd46e3c0; HJ_SSID_3=ra4zlx-5ee0-43a1-b8d9-269d60aa68a8; HJ_CST=0; HJ_CSST_3=1'
]


proxies = [
  "http://58.234.116.100:80",
  "http://91.202.230.219:8080",
  "http://110.141.192.123:80",
  "http://51.79.40.227:80",
  "http://95.138.193.63:80",
  "http://144.91.97.235:80",
  "http://149.156.33.134:80",
  "http://14.7.183.127:80",
  "http://80.39.228.110:80"
]

#  
TIMEOUT = 30
# 重连次数
MAX_RETRIES = 3


# get获取請求数据
def get_content(url):
  resp = None
  try:
    session = requests.session()   
    session.keep_alive = False # 设置连接活跃状态为False
    #设置重连次数
    session.mount('http://', HTTPAdapter(max_retries=MAX_RETRIES))
    session.mount('https://', HTTPAdapter(max_retries=MAX_RETRIES))
    
    headers['User-Agent'] = useragents[random.randint(0, len(useragents)-1)]
#     resp = session.get(url, headers=headers, timeout=TIMEOUT)
    resp = session.get(url, headers=headers, proxies={'http': proxies[random.randint(0, len(proxies)-1)]}, timeout=TIMEOUT)
    resp.raise_for_status()   # 如果返回的状态码不是200， 则抛出异常;
    resp.encoding = resp.apparent_encoding  # 判断网页的编码格式， 便于respons.text知道如何解码;
  except Exception as ex:
    print(ex)
  else:
    resp.close()  # 注意关闭response 
    return resp


# post获取請求数据
def post_content(url,data):
  resp = None
  try:
    session = requests.session()   
    session.keep_alive = False # 设置连接活跃状态为False
    #设置重连次数
    session.mount('http://', HTTPAdapter(max_retries=MAX_RETRIES))
    session.mount('https://', HTTPAdapter(max_retries=MAX_RETRIES))
    
    headers['User-Agent'] = useragents[random.randint(0, len(useragents)-1)]
#     resp = session.post(url, data=data, headers=headers, timeout=TIMEOUT)
    resp = session.post(url, data=data, headers=headers, proxies={'http': proxies[random.randint(0, len(proxies)-1)]}, timeout=TIMEOUT)
    resp.raise_for_status()   # 如果返回的状态码不是200， 则抛出异常;
    resp.encoding = resp.apparent_encoding  # 判断网页的编码格式， 便于respons.text知道如何解码;
  except Exception as ex:
    print(ex)
  else:
    resp.close()  # 注意关闭response  
    return resp



"""
查詢單詞   https://www.mojidict.com/

:param wbname:
:param data: 往excel中存储的数据;
:param sheetname:
:return:
"""
def search_moji_dict(word):
  searchText = word.spell
  if searchText:
    url = 'https://api.mojidict.com/parse/functions/search_v3'
    payload =   {
        "searchText": searchText,
        "needWords": 'true',
        "langEnv": "zh-CN_ja",
        "_ApplicationId": "E62VyFVLMiW7kvbtVq3p"
    }
    resp = post_content(url, json.dumps(payload))
#     print(searchText , r.text)
    result = json.loads(resp.text);
#     print(result["result"]["words"])
    
    if len(result["result"]["words"]) > 0 :     
      originalSearchText = result["result"]["originalSearchText"]
      searchText = result["result"]["searchResults"][0]["searchText"]
      spell = result["result"]["words"][0]["spell"]
      pron = result["result"]["words"][0]["pron"]

      # 較驗 假名(读音) 是否一致
      if originalSearchText == searchText and spell == searchText and word.pron == pron : 
        #獲取 声调
        if not word.accent and "accent" in result["result"]["words"][0] and len(result["result"]["words"][0]["accent"]) > 0 :
          word.accent = result["result"]["words"][0]["accent"]
          
        #獲取 詞性
        if "excerpt" in result["result"]["words"][0]:
          excerpt = result["result"]["words"][0]["excerpt"]
#         else:
#           excerpt = ''
        pattern = re.compile("^\[(.*?)\](.*)", re.MULTILINE | re.DOTALL) 
        # pattern.search(excerpt).groups()
        picker = pattern.search(excerpt)
        if picker:
          picker = picker.groups()
          if not word.word_class:
            word.word_class = picker[0]
          if not word.meanings:
            word.meanings = picker[1]
          
        #獲取 例句
        # objectId  https://www.mojidict.com/details/198963336
        objectId = result["result"]["words"][0]["objectId"]
        if not word.sentence or not word.translation :
          # 创建soup对象 
          soup = BeautifulSoup(get_content('https://www.mojidict.com/details/' + objectId).content, "html.parser") 
          example = soup.find('div', {'class': 'example-info'})
#           print(example)
          #例文          
          example_item = []
          if example:
            for i,child in enumerate(example.contents):
              if hasattr(child, 'div'):
                if child.string:
                  example_item.append(child.string.strip())
                else:
                  soup = BeautifulSoup(child.decode(), "html.parser") 
                  ruby = ''
                  for rb in soup.select('ruby rb'):
                    ruby = ruby + str(rb.text.split()[0])
                  example_item.append(ruby)
          
          if len(example_item) > 0 and not word.sentence:
            word.sentence = example_item[0]
            word.translation = example_item[1]


# 查詢單詞  https://dict.hjenglish.com
def search_hjclass_dict(word):
  searchText = word.spell
  
  if searchText:
    headers['Cookie'] = cookies[random.randint(0, len(cookies)-1)]
    url = 'https://dict.hjenglish.com/jp/jc/' + searchText
        
    resp = get_content(url)
    # 获取状态 
#     print(url, resp.status_code)
#     print(response.content.decode())

    # 创建soup对象 
    soup = BeautifulSoup(resp.text, "html.parser") 
#     example = soup.find('div', {'class': 'word-details '})

    # 多種讀音
    if len(soup.select('header.word-details-header ul div.pronounces span.pronounce-value')) > 0 : 
      for item in soup.select('section.word-details-content div.word-details-pane'): 
        soup = BeautifulSoup(item.decode(), "html.parser") 
        #字符串截取
        if soup.select('div.word-info div.pronounces span')[0].text.strip()[1:-1] == word.pron: 
          break;
    elif len(soup.select('div.word-details div.word-details-pane')) > 0 : 
      soup = BeautifulSoup(soup.select('div.word-details div.word-details-pane')[0].prettify(), "html.parser")    
     
    #單詞
    if len(soup.select('div.word-info div.word-text h2')) > 0 :
      spell = soup.select('div.word-info div.word-text h2')[0].text.strip()
    
      if spell == searchText: 
        #發音
        pronounces = soup.select('div.pronounces span')
        if len(pronounces) == 4 : 
          pron = pronounces[0].text.strip()[1:-1] #字符串截取
#           print(pronounces[1].text.strip()[1:-1])
          
          # 較驗 假名(读音) 是否一致
          if pron and word.pron and not pron == word.pron:
            print("word search not found ! ", word.spell, " or ", word.pron , " have error !")
            return
              
          # 声调
          if not word.accent:
            word.accent = pronounces[2].text.strip()
#           print(pronounces[3].attrs['data-src'])
        
        #詞性
        if not word.word_class and len(soup.select('div.simple h2')) > 0 :
          word.word_class = soup.select('div.simple h2')[0].text.strip()[1:-1]
            
        #詞义
        meanings = soup.select('div.simple ul li')
        word_meanings = ''
        for meaning in meanings:
          word_meanings = word_meanings + ";".join(meaning.text.split()) 
        if not word.meanings:
          word.meanings = word_meanings
        
        #例句
        example_sentence = soup.select('div.word-details-item-content section.detail-groups p.def-sentence-from')
        example_sentence = (example_sentence[0].text.strip() if (len(example_sentence) > 0) else '')
        
        example_translation = soup.select('div.word-details-item-content section.detail-groups p.def-sentence-to')
        example_translation = (example_translation[0].text.strip() if (len(example_translation) > 0) else '')
        
        # 汉字  假名(读音) 声调   词性   词义   文節（詞組）   意味
        if not word.sentence:
          word.sentence = example_sentence
        if not word.translation:
          word.translation = example_translation


if __name__ == "__main__":    
  
#   res=doExcel("D:/back/N1必背.xlsx","平仮名").get_data()
  words = ExcelHandler("D:/back/N1必背.xlsx").get_data()
  print(words)
  
  # 爬取要素
  for word in words:
    if word.need_fix():
      print(word)
      search_moji_dict(word)
      if word.need_fix():
        search_hjclass_dict(word)
      print(word)
      
  ExcelHandler.create_to_excel('D:/back/hello.xlsx', words)


