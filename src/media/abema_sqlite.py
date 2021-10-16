#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:      test
# Date:      2020/4/14
__Author__ = 'chen'
#-------------------------------------------------------------------------------

import os
import re
import socks
import socket
import base64
import requests
import threading
import sqlite3
from enum import Enum, unique
from Crypto.Cipher import AES
from Crypto import Random
from concurrent.futures import ThreadPoolExecutor
from itertools import product
import m3u8


# 狀態   -1: 失敗   ;0 下載 ; 1 成功
@unique
class Status(Enum):
  FAILURE = -1
  INIT = 0
  SUCCESS = 1


# 配置headers防止被墙，一般问题不大
headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
}

proxies = {
  'http': 'socks5://127.0.0.1:8580',
  'https': 'socks5://127.0.0.1:8580'
}

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 7027)
socket.socket = socks.socksocket

  
dbfile = 'D:/Database/SQLite/hls.db'
tablename = 'ABEMA'
dpath = 'D:/Back/'


# 初始化下載信息
def init_hls(title,url,key):
  print("初始化下載信息 ...")
  # 连接数据库(如果不存在则创建)
  conn = sqlite3.connect(dbfile)
  
  #创建游标对象
  cursor = conn.cursor()
  try:
    #  判断表是否存在的方法，获取一条数据
    sql = "select count(*) from sqlite_master where type='table' and name = ?"
    #获取结果集合，获取一条数据
    value = cursor.execute(sql, (tablename,)).fetchone()
    if value and value[0] == 0:
      # 创建表
      sql = 'CREATE TABLE '+ tablename +'(id integer PRIMARY KEY autoincrement, title varchar(100), url text, key varchar(30) , iv varchar(30), status integer)'
      cursor.execute(sql)
    
    # 插入数据
    data = (title,url,key) # or ['love2', 2221]
    sql = "INSERT INTO "+ tablename +"(title,url,key) VALUES(?, ?, ?)"
    cursor.execute(sql, data)
  except Exception as e:
    print(e)
    print("数据初始化失败　:" ,title,url,key)
    exit(1)
  finally:
    # 关闭游标
    cursor.close()
    # 提交事物
    conn.commit()
    # 关闭连接
    conn.close()



# 獲取下載鏈接
def get_hls():
  print("獲取下載鏈接 ...")
#   conn = sqlite3.connect('testDB.db')
  conn = sqlite3.connect(dbfile)
  
  #创建游标对象
  cursor = conn.cursor()
  try:
    # 查询数据
    sql = "select * from " + tablename + " where status is not ?"
    # fixed  Cannot operate on a closed cursor
    values = [x for x in cursor.execute(sql,(Status.SUCCESS.value,))]
    return values
  except Exception as e:
    print(e)
    print("獲取下載鏈接失败")
    exit(1)
  finally:
    # 关闭游标
    cursor.close()
    # 提交事物
    conn.commit()
    # 关闭连接
    conn.close()


# 更新狀態   update sqlite status  
def upate_status(pk, status):
  print("更新狀態 ...")
  conn = sqlite3.connect(dbfile)
  
  #创建游标对象
  cursor = conn.cursor()
  try:
    # 查询数据
    sql = "update " + tablename + " set status = ?  where id = ?"
    cursor.execute(sql, (status.value, pk))
  except Exception as e:
    print(e)
    print("更新狀態失败 " , pk, status)
    exit(1)
  finally:
    # 关闭游标
    cursor.close()
    # 提交事物
    conn.commit()
    # 关闭连接
    conn.close()



# 下载ts媒体文件
def download(minyami):
  try:
    pk = minyami[0]
    title = minyami[1]
    url = minyami[2]
    password = minyami[3]
    print(url,password,title)
    
    # 開始下載 更新狀態
    upate_status(pk, Status.INIT)
    
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
      
    # 開始下載 更新狀態 
    upate_status(pk, Status.SUCCESS)
  except Exception as ex:
    print(ex)
    print("download failed ：" + url )
    upate_status(pk, Status.FAILURE)
    exit(1)



if __name__ == '__main__':
  
  http_client = m3u8.httpclient.DefaultHTTPClient()
  
  # 创建线程的线程池
  executor = ThreadPoolExecutor(max_workers=1)
  
    
  # minyami -d "https://ds-vod-abematv.akamaized.net/program/30-5_s4_p74/180/playlist.m3u8?aver=1&ccf=26&dt=pc_unknown&dtid=jdwHcemp6THr&enc=clear" --output "進撃の巨人 - The Final Season - 74話 (アニメ)  無料動画・見逃し配信を見るなら  ABEMA.ts" --key "e77391787d2ad2d73ad2e823e686e91e"
  # 匹配双引号的正则表达式
  pattern = re.compile('(?<=\").*?(?=\")', re.MULTILINE | re.DOTALL)
  while True:
    minyami = input('请输入视频的minyami信息: ').strip()
    print(minyami)
    if not minyami: 
      break
    minyami = pattern.findall(minyami)
    print(minyami)
    url = minyami[0]
    title = (minyami[2].split('-')[2]).split(' ')[1]
    key = minyami[4]
    print(url,key,title)
    #初始化下載信息
    init_hls(title,url,key)
    
#     t = threading.Thread(target=download,args=(url,password,title)) 
#     t.start()

  # 獲取下載信息
  values = get_hls()
  for minyami in values:
    print(minyami)
#     download(minyami)
    # 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞
    executor.submit(download, minyami)
    
  # 相当于进程池的pool.close() pool.join()
  executor.shutdown()  
  
  
  
  
  