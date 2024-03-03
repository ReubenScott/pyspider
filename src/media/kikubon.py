#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:      test_socks
# Date:      2020/4/14
__Author__ = 'Negoo_wen'
#-------------------------------------------------------------------------------

import os
import shutil
import base64
import traceback
import requests
from requests.adapters import HTTPAdapter
from Crypto.Cipher import AES
import m3u8
import ffmpeg 

# 配置headers防止被墙，一般问题不大  '': '',
headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'en-US,en;q=0.5',
  'Connection': 'keep-alive',
  'Cookie': 'kikubonses=k5cmvdu28mp5k0bip37ceu3q0c; login20160719=7bba5eb67ba0bc9c0568348ef1b34b396fe476fb; __c__login20160719=4f636fc56a71d6f094aceed9139f699cebc17ebb; _ga=GA1.2.1281779443.1694432659; _ga_T5Y24ZQPY9=GS1.2.1694432659.1.0.1694432659.0.0.0; browsingData=%7B%220%22%3A%22830%22%2C%223%22%3A%22552%22%2C%224%22%3A%22776%22%2C%226%22%3A%22638%22%2C%228%22%3A%22453%22%2C%2210%22%3A%22502%22%2C%2211%22%3A%22135%22%2C%2214%22%3A%22819%22%7D',
}

timeout = 10


# Extract MP3 audio from Videos
def video_to_mp3_bak(file_name):
  """ Transforms video file into a MP3 file """
  try:
    file, extension = os.path.splitext(file_name)
    dir_path = os.path.dirname(file_name)
    file_title = os.path.basename(file)
    wav_file = base64.b64encode(bytes(file_title, 'utf-8'))
    wav_file = os.path.join(dir_path, str(wav_file, encoding="utf-8"))
    # Convert video into .wav file
    os.system('ffmpeg -i {file}{ext} {tmp}.wav'.format(file=file, ext=extension, tmp=wav_file))
    # Convert .wav into final .mp3 file
    os.system('lame {tmp}.wav {file}.mp3'.format(file=file, tmp=wav_file))
    os.remove('{}.wav'.format(wav_file))  # Deletes the .wav file
    print('"{}" successfully converted into MP3!'.format(file_name))
  except:
    print(traceback.format_exc())
    exit(1)

 
# Extract MP3 audio from Videos
def video_to_mp3(file_name):
  """ Transforms video file into a MP3 file """
  try:
    file, extension = os.path.splitext(file_name)
    dir_path = os.path.dirname(file_name)
    file_title = os.path.basename(file)
    # 入力 
    stream = ffmpeg.input(os.path.join(dir_path, file_title + extension))
    # 出力 
    stream = ffmpeg.output(stream, os.path.join(dir_path, file_title + ".mp3"))
    # 実行 
    ffmpeg.run(stream, quiet=True, overwrite_output=True)
    print('"{}" successfully converted into MP3!'.format(file_name))
  except:
    print(traceback.format_exc())
    exit(1)

  
# 
# url = "https://kikubon.jp/mlist.php?asKey=4097&.m3u8"
# title = input('请输入保存文件名: ').strip()
# Extract MP3 audio from Videos
# 下载ts媒体文件
def download_audio(url, dpath, file_name, cookie=None):
  try:
    url = url.strip()
    title = file_name.strip()
    
    # 保存目录未选择检验
    assert dpath and dpath.strip() != "", "保存目录未设置"
    
    if cookie:
      headers["Cookie"] = cookie.strip()
    
    # 创建线程的线程池
    session = requests.session()   
    session.keep_alive = False  # 设置连接活跃状态为False
    # 设置重连次数
    # session.mount('http://', HTTPAdapter(max_retries=3))
    # session.mount('https://', HTTPAdapter(max_retries=3))
    adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=10)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    http_client = m3u8.httpclient.DefaultHTTPClient()
    
    playlist = m3u8.load(url, http_client=http_client, headers=headers) 
    print(playlist.dumps())
    
    # 取得key 16位密钥    
    # EXT-X-KEY:METHOD=AES-128,URI="abematv-license://2mznKG7uJBm8NFeojhh1rH",IV=0x0e9ff06f46ffda25228ffd6b7369cb2a
    for key in playlist.keys:
      if key:  # First one could be None
        key.uri
        key.method
    
    rsp = session.get(key.uri, headers=headers, allow_redirects=True)
    # history追踪页面重定向历史
    reditList = rsp.history  # 可以看出获取的是一个地址序列
    # 获取重定向最终的url
    redit_url = reditList[len(reditList) - 1].headers["location"]
    
    rsp = session.get(redit_url, headers=headers)
    password = rsp.content
    # 初始化AES     
    cipher = AES.new(password, AES.MODE_CBC, password)
    
    # EXTINF  TS地址提取
    media_url_list = []
    media_ts_name = []
    for i in playlist.segments:
      surl = str(i).split('\n')[-1]
      media_url_list.append(surl)
      
    print(media_url_list)
    
    # 用来保存ts文件 
    ts_dir = base64.b64encode(bytes(title, 'utf-8'))
    ts_dir = os.path.join(dpath, '.ts/', str(ts_dir, encoding="utf-8"))
    if not os.path.exists(ts_dir): 
      os.makedirs(ts_dir)
        
    # 下载ts媒体文件
    for index, ts_url in enumerate(media_url_list):
      ts_name = str(index) + '.ts'
      print(ts_name, ts_url)
      media_ts_name.append(ts_name)
      
      # 下载ts媒体文件
      rsp = session.get(ts_url, headers=headers, allow_redirects=True, timeout=timeout)
      # history追踪页面重定向历史
      reditList = rsp.history  # 可以看出获取的是一个地址序列
      # 获取重定向最终的url
      redit_url = reditList[len(reditList) - 1].headers["location"]
      
      # 关闭请求 释放内存 
      rsp.close() 
      del(rsp)
      
      # 下载ts媒体文件
      rsp = session.get(redit_url, headers=headers, timeout=timeout)
      con = rsp.content
      if cipher:  # 解密
        con = cipher.decrypt(rsp.content)
        
      # 关闭请求 释放内存 
      rsp.close() 
      del(rsp)
        
      with open(os.path.join(ts_dir , ts_name), 'wb') as fw:
        fw.write(con)
    
    print(media_ts_name)
    video_path = os.path.join(dpath, title + '.mp4') 
    if os.path.exists(video_path): 
      os.remove(video_path)
      
    # 合并ts文件转化为视频文件
    with open(video_path , 'ab') as fw:
      for ts_name in media_ts_name:
        with open(os.path.join(ts_dir , ts_name), 'rb') as fr:
          fw.write(fr.read())

    # convert mp4 to mp3 
    video_to_mp3(video_path)

    # 刪除ts文件
    audio_path = os.path.join(dpath, title + '.mp3') 
    if os.path.exists(audio_path): 
      os.remove(video_path)
      shutil.rmtree(ts_dir)
    else:
      print("Extract MP3 failed ：" + video_path)
    return True  
  except:
    print(traceback.format_exc())
    print("download failed ：" + url)
    return False
  finally:
    # 关闭會話 释放内存 
    session.close()
    del(session)

   
if __name__ == '__main__':
    dpath = 'D:/Back/'
    # "https://kikubon.jp/mlist.php?asKey=4097&.m3u8"
    url = input('请输入音频的HLS信息: ').strip()
    title = input('请输入保存文件名: ').strip()
    download_audio(url, dpath, title)
  
