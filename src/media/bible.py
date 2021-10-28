#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import re
import os
import time
import sys
from bs4 import BeautifulSoup, SoupStrainer

# 配置请求头
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.607 Yowser/2.5 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive',
  'sec-ch-ua' : 'Chromium";v="92", " Not A;Brand";v="99", "Yandex";v="21',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'cache-control': 'max-age=0',
  'cookie': 'locale=ja; _youversion-web_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTcyNWFkNzQ4Nzg5NTk0NjdiOGMxMDY0YTBhYzdhYTg0BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUY3K3U0WHUxeG5jSkZydkpwK0FER1E3Y1owcXdaY3BqdDhBNFl5WStCMmc9BjsARg%3D%3D--459900ddbb04349ceb1795c263c90dacebb225df; last_read=GEN.1; _s=amp-rgvPx3FJWGmOrvZwwP8Bdg; version=1819; www2=1; OAUTH=%7B%7D; G_ENABLED_IDPS=google'
}

timeout=30

# 'D:/bible'  '/home/app/Bible'
basepath = 'D:/bible'

# 配置请求头 url  'https://www2.bible.com/ja/bible/83/%s.%s.JCB?show_audio=1'
bible_dict = {
  'JCB': 'https://www2.bible.com/ja/bible/83/%s.%s.JCB?show_audio=1',
  'NASB': 'https://www2.bible.com/bible/100/%s.%s.nasb1995?show_audio=1',
  'ESV': 'https://www2.bible.com/bible/59/%s.%s.esv?show_audio=1',
  '新共同訳': 'https://www2.bible.com/bible/1819/%s.%s.新共同訳?show_audio=1'
}


# 获取請求数据
def get_content(url):
  response = None
  while True:      
    try:
      response = requests.get(url, headers=headers, timeout=timeout)   # 响应时间
      response.raise_for_status()   # 如果返回的状态码不是200， 则抛出异常;
      response.encoding = response.apparent_encoding  # 判断网页的编码格式， 便于respons.text知道如何解码;
    except Exception as ex:
      time.sleep(0.5)
      print(ex)
    else:
      response.close()  # 注意关闭response  
      return response.content


# 获取章節数据   url = 'https://www2.bible.com/ja/bible/83/GEN.2.JCB?show_audio=1'
def parse_chapter(book, index, title):  
  url = url_template %(book,1)
  #GEN 1 創世記 https://www2.bible.com/ja/bible/83/GEN.1.JCB?show_audio=1
  print(book, index, title, url)   

  book_dir =  dirpath + '/' + str(index) + ' ' + title

  # 创建soup对象
  soup = BeautifulSoup(get_content(url), "html.parser")  

  #章節  <div data-reactid="110">1</div>     is Number
  chapters = soup.select('div.chapter-container ul.chapter-list li div')
  for chapter in chapters:       
    if chapter.string.isdigit():
      audio_download(book_dir, title + chapter.string  + '.mp3' , url_template %(book, chapter.string))


# 下载
def audio_download(book_dir, audio_name, url):
  #print(book_dir, audio_name, url)

  # 创建soup对象
  soup = BeautifulSoup(get_content(url), "html.parser", parse_only=SoupStrainer('audio'))
  # 解析数据  div.audio-player > audio > source:nth-of-type(2)
  mp3url = "https:" + soup.select('source')[1].get('src')     
  mp3path = book_dir + '/' + audio_name
  print('download: ', mp3path , mp3url)

  if not os.path.exists(book_dir):
    os.makedirs(book_dir)

  with open(mp3path, 'wb') as fp:
    while True:      
      try:
        response = requests.get(mp3url,timeout=timeout)
        fp.write(response.content)
      except Exception as ex:
        time.sleep(0.5)
        print(ex)
      else:
        response.close()  # 注意关闭response  
        break     

if __name__ == "__main__":
  # nohup python bible.py NASB &
  args = sys.argv
  if len(args) != 2:
    print('Fail, params error, try: python', args[0], 'your_bible_version') 
    print('eg: python', args[0], 'NASB')
    exit(1)
  
  # bible version args : 'JCB' 
  bible_version = args[1] 
  dirpath = basepath + '/' + bible_version
  url_template = bible_dict[bible_version]
  
  
  #url = 'https://www2.bible.com/ja/bible/83/GEN.2.JCB?show_audio=1'
  url = url_template %('GEN',1)

  soup = BeautifulSoup(get_content(url), "html.parser")  

  '''
  script = soup.findAll("script" , attrs={"type": "application/javascript"})  
  #基于enumerate的项和索引
  for i,name in enumerate(script):
    print('index is %s,name is %s' %(i,name))  
  '''

  #獲取javascript 中Json書物  soup.findAll('script')[11].string.encode('utf8')  
  pattern = re.compile("window.Bible.__INITIAL_STATE__ = ({.*?});$", re.MULTILINE | re.DOTALL)      
  script = soup.findAll('script' , attrs={"type": "application/javascript"} , text=pattern)[0].string

  #print(pattern.search(script).group(1))  
  picker = json.loads(pattern.search(script).group(1))  

  #書物  
  booklist = soup.select('div.book-container ul.book-list > li')

  # 遍历键值对
  for book,index in picker["bibleReader"]["books"]["map"].items():       
    parse_chapter(book, index + 1 , booklist[index].string )  

