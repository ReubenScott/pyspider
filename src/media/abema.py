#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:      test_socks
# Date:      2020/4/14
__Author__ = 'Negoo_wen'
#-------------------------------------------------------------------------------

import os
import re
import socks
import socket
import base64
import requests
import threading
from Crypto.Cipher import AES
from Crypto import Random
from concurrent.futures import ThreadPoolExecutor
from itertools import product
import m3u8


# 配置headers防止被墙，一般问题不大
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
  }

proxies = {
  'http': 'socks5://127.0.0.1:8580',
  'https': 'socks5://127.0.0.1:8580'
}


# 下载ts媒体文件
def download(minyami):
  try:
    minyami = pattern.findall(minyami)
    print(minyami)
    url = minyami[0]
    title = (minyami[2].split('-')[2]).split(' ')[1]
    password = minyami[4]
    print(url,password,title)
    
    playlist = m3u8.load(url, http_client=http_client)  # this could also be an absolute filename
    print(playlist.dumps())
    
    
    # 取得key 16位密钥    
    #EXT-X-KEY:METHOD=AES-128,URI="abematv-license://2mznKG7uJBm8NFeojhh1rH",IV=0x0e9ff06f46ffda25228ffd6b7369cb2a
    for key in playlist.keys:
      if key:  # First one could be None
        key.uri
        key.method
        iv_key = bytes.fromhex(key.iv[2:])
    
	#   message_bytes = base64.b16decode(iv_hex.upper())
	#   print(message_bytes)
	#   iv_key =  base64.encodebytes(message_bytes)
    
    password = bytes.fromhex(password)
    # 初始化AES    
    cipher = AES.new(password,AES.MODE_CBC,iv_key)
    
    #EXTINF  TS地址提取
    media_url_list = []
    media_ts_name = []
    for i in playlist.segments:
      surl = str(i).split('\n')[-1]
      lurl = 'https://ds-vod-abematv.akamaized.net' + surl
      media_url_list.append(lurl)
      
    print(media_url_list)
    
    # 用来保存ts文件 
    ts_dir = os.path.join(dpath,'.ts/') 
    if not os.path.exists(ts_dir): 
    	os.mkdir(ts_dir)
    
    # 下载ts媒体文件
    pattern_ts = re.compile('.*\/(.*\.ts)', re.MULTILINE | re.DOTALL)
    for ts_url in media_url_list:
      ts_name = pattern_ts.findall(ts_url)[0]
      media_ts_name.append(ts_name)
      print(ts_name, ts_url)
      # 下载ts媒体文件
      con = requests.get(ts_url).content
      if cipher: # 解密
        con = cipher.decrypt(con)
      with open(ts_dir + ts_name, 'wb') as fw:
        fw.write(con)
	
	
    # 合并ts文件转化为视频文件
    print(media_ts_name)
    with open(dpath  + title + '.mp4' , 'ab') as fw:
      for ts_name in media_ts_name:
        with open(ts_dir+ ts_name, 'rb') as fr:
          fw.write(fr.read())

    # 刪除ts文件
    for ts_name in media_ts_name:
      os.remove(ts_dir + ts_name)
  except Exception as ex:
    print(ex)
    print("download failed ：" + url)



if __name__ == '__main__':
	
  socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 7027)
  socket.socket = socks.socksocket
  http_client = m3u8.httpclient.DefaultHTTPClient()
  
  # 创建线程的线程池
  executor = ThreadPoolExecutor(max_workers=2)
  
  dpath = 'D:/Back/'
  
  # minyami -d "https://ds-vod-abematv.akamaized.net/program/30-5_s4_p74/180/playlist.m3u8?aver=1&ccf=26&dt=pc_unknown&dtid=jdwHcemp6THr&enc=clear" --output "進撃の巨人 - The Final Season - 74話 (アニメ)  無料動画・見逃し配信を見るなら  ABEMA.ts" --key "e77391787d2ad2d73ad2e823e686e91e"
	# 匹配双引号的正则表达式
  pattern = re.compile('(?<=\").*?(?=\")', re.MULTILINE | re.DOTALL)
  while True:
    minyami = input('请输入视频的minyami信息: ')
    print(minyami)
    if not minyami: 
      break
     
#     t = threading.Thread(target=download,args=(url,password,title)) 
#     t.start()

    # 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞
    executor.submit(download, minyami)
    
  # 相当于进程池的pool.close() pool.join()
  executor.shutdown()  
  
  
  