#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request, urllib.error, urllib.parse
import os, sys, datetime, argparse, re
import subprocess
import base64
import shlex
import logging
from sys import argv



logging.basicConfig(level=logging.DEBUG )
handler = urllib.request.HTTPHandler(debuglevel=0)
opener = urllib.request.build_opener(handler)
urllib.request.install_opener(opener)


auth_token = ""
auth_key = "bcd151073c03b352e1ef2fd66c32209da9ca0afa" ## 現状は固定・
key_lenght = 0
key_offset = 0

def auth1():
    url = "https://radiko.jp/v2/api/auth1"
    headers = {}
    auth_response = {}

    headers = {
        "User-Agent": "curl/7.56.1",
        "Accept": "*/*",
        "X-Radiko-App":"pc_html5" ,
        "X-Radiko-App-Version":"0.0.1" ,
        "X-Radiko-User":"dummy_user" ,
        "X-Radiko-Device":"pc" ,
    }
    req = urllib.request.Request( url, None, headers  )
    res = urllib.request.urlopen(req)
    auth_response["body"] = res.read()
    auth_response["headers"] = res.info()
    return auth_response

def get_partial_key(auth_response):
    authtoken = auth_response["headers"]["x-radiko-authtoken"]
    offset    = auth_response["headers"]["x-radiko-keyoffset"]
    length    = auth_response["headers"]["x-radiko-keylength"]
    offset = int(offset)
    length = int(length)
    partialkey= auth_key[offset:offset+length]
    partialkey = base64.b64encode(partialkey.encode())

    # logging.info(f"authtoken: {authtoken}")
    # logging.info(f"offset: {offset}")
    # logging.info(f"length: {length}")
    # logging.info(f"partialkey: {partialkey}")

    return [partialkey,authtoken]

def auth2( partialkey, auth_token ) :
    url = "https://radiko.jp/v2/api/auth2"
    headers =  {
        "X-Radiko-AuthToken": auth_token,
        "X-Radiko-Partialkey": partialkey,
        "X-Radiko-User": "dummy_user",
        "X-Radiko-Device": 'pc' # 'pc' 固定
    }
    req  = urllib.request.Request( url, None, headers  )
    res  = urllib.request.urlopen(req)
    txt = res.read()
    area = txt.decode()
    print(txt)
    return area

def gen_temp_chunk_m3u8_url( url, auth_token ):
    headers =  {
        "X-Radiko-AuthToken": auth_token,
    }
    req  = urllib.request.Request( url, None, headers  )
    res  = urllib.request.urlopen(req)
    body = res.read().decode()
    lines = re.findall( '^https?://.+m3u8$' , body, flags=(re.MULTILINE) )
    # embed()
    return lines[0]


res = auth1()
ret = get_partial_key(res)
token = ret[1]
partialkey = ret[0]
auth2( partialkey, token )
url = 'http://f-radiko.smartstream.ne.jp/ABC/_definst_/simul-stream.stream/playlist.m3u8'
m3u8 = gen_temp_chunk_m3u8_url(url ,token)

os.system("ffplay -nodisp -loglevel quiet -headers 'X-Radiko-Authtoken:{token}' -i '{m3u8}'")
#print( f"curl -v  -H 'X-Radiko-Authtoken:{data['token']}' '{data['url']}'   " )

