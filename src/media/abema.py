#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:      test
# Date:      2020/4/14
__Author__ = 'chen'
#-------------------------------------------------------------------------------

import os
import io
import re
import socks
import socket
import base64
import shutil
import threading
import sqlite3
import requests
from requests.adapters import HTTPAdapter
from enum import Enum, unique
from Crypto.Cipher import AES
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import m3u8


# 狀態   -1: 失敗   ;0 下載 ; 1 成功
@unique
class Status(Enum):
  FAILURE = -1
  INIT = 0
  SUCCESS = 1


# 配置headers防止被墙，一般问题不大
headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
  'Connection': 'close'
}

proxies = {
  'http': 'socks5://127.0.0.1:8580',
  'https': 'socks5://127.0.0.1:8580'
}

# 連接超時時間(秒)
TIMEOUT=10
# 线程個數
MAX_WORKERS=3
# 设置重连次数
MAX_RETRIES=5

# global socket proxy
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 7027)
socket.socket = socks.socksocket
socket.setdefaulttimeout(TIMEOUT)
  
# local 
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
  print("更新狀態開始 ...", pk, status)
  conn = sqlite3.connect(dbfile)
  
  #创建游标对象
  cursor = conn.cursor()
  try:
    # 查询数据
    sql = "update " + tablename + " set status = ?  where id = ?"
    cursor.execute(sql, (status.value, pk))
  except Exception as e:
    print(e)
    print("更新狀態失败 ..." , pk, status)
    exit(1)
  else:
    print("更新狀態成功...", pk, status)
  finally:
    # 关闭游标
    cursor.close()
    # 提交事物
    conn.commit()
    # 关闭连接
    conn.close()



# 信号量
sema = True


# 下载ts媒体文件
def download(minyami):
  try:
    # 创建线程的线程池
    executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
    global sema
    sema = True
    
    pk = minyami[0]
    title = minyami[1]
    url = minyami[2]
    password = minyami[3]
    print(url,password,title)
    
    # 開始下載 更新狀態
    upate_status(pk, Status.INIT)
    
    playlist = m3u8.load(url, http_client=http_client)  # this could also be an absolute filename
#     print(playlist.dumps())
    
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
    ts_name = base64.b64encode(bytes(title, 'utf-8'))
    ts_dir = os.path.join(dpath, '.ts/', str(ts_name, encoding = "utf-8").replace('/',''))
    if not os.path.exists(ts_dir): 
      os.mkdir(ts_dir)
    
  
    # 下载ts媒体文件 
#     requests.adapters.DEFAULT_RETRIES = 5
    session = requests.session()   
    session.keep_alive = False # 设置连接活跃状态为False
    #设置重连次数
    session.mount('http://', HTTPAdapter(max_retries=MAX_RETRIES))
    session.mount('https://', HTTPAdapter(max_retries=MAX_RETRIES))
    
    pbar = tqdm(total=len(media_url_list), initial=1, unit='Piece', unit_scale=True, desc='Processing: ')
    pattern_ts = re.compile('.*\/(.*\.ts)', re.MULTILINE | re.DOTALL)
    for ts_url in media_url_list:
      ts_name = pattern_ts.findall(ts_url)[0]
      media_ts_name.append(ts_name)
#       print(ts_name, ts_url)
      # 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞
      futrue = executor.submit(down_from_url, session, ts_url, os.path.join(ts_dir , ts_name) , pbar)
      futrue.add_done_callback(callback)
      '''
      # 下载ts媒体文件
      if False == down_from_url(ts_url, os.path.join(ts_dir , ts_name)):
        upate_status(pk, Status.FAILURE)
        return
      pbar.update(1)
      '''
  
    # 相当于进程池的pool.close() pool.join()
    executor.shutdown()  
    session.close()
    del(session)
  
    if sema:
      # 合并ts文件转化为视频文件
      video_path = os.path.join(dpath, title + '.mp4') 
      if os.path.exists(video_path): 
        os.remove(video_path)
      
      with open(video_path, 'ab') as fw:
        for ts_name in media_ts_name:
          with open(os.path.join(ts_dir, ts_name), 'rb') as fr:
            if cipher: # 解密
              fw.write(cipher.decrypt(fr.read()))
            else:
              fw.write(fr.read())
              
      # 刪除ts文件夹
      shutil.rmtree(ts_dir)
          
      # 開始下載 更新狀態 
      upate_status(pk, Status.SUCCESS)
  except Exception as ex:
    print(ex)
    print("download failed ：" + url )
    upate_status(pk, Status.FAILURE)
#     exit(1)


#  requests 下载文件
def down_from_url(session, url, dst , pbar):
  global sema 
  if sema:
    try:
      response = session.get(url, headers=headers, stream=True, timeout=TIMEOUT)
      total_size = int(response.headers['Content-Length'])
        
      if os.path.exists(dst):
        file_size = os.path.getsize(dst)
        if file_size == total_size:
          pbar.update(1)
          return True
      #header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
      
      with open(dst, 'wb') as of:
        for chunk in response.iter_content(chunk_size=1024):
          if chunk:
            of.write(chunk)
            
      
      # 下载完毕后我会使用如下方式和上面的 total_size 进行对比
      with open(dst, 'r') as f:
        if isinstance(f, io.TextIOBase):
          length = os.fstat(f.fileno()).st_size
            
    except Exception as ex:
      print(ex)
      return False
    else:
      pbar.update(1)
      return total_size == length
    finally:
      # 关闭请求 释放内存 
      response.close() 
      del(response)
      


#  requests 下载回調
def callback(future): 
  global sema
  result = future.result() 
  cur_thread = threading.current_thread().name 
  # 下载ts媒体文件
  if False == result:      
    sema = False
#     upate_status(pk, Status.FAILURE)



if __name__ == '__main__':
  
  http_client = m3u8.httpclient.DefaultHTTPClient()
  
    
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
    download(minyami)
  
  
  
  
  