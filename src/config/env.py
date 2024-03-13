#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from peewee import SqliteDatabase

db = SqliteDatabase('E:/Documents/market.db')

# , pragmas={
# 'journal_mode': 'wal',
# 'cache_size': -1 * 64000,  # 64MB
# 'foreign_keys': 1,
# 'ignore_check_constraints': 0,
# 'synchronous': 0}

#模擬header的user-agent
useragents = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0'
]

# 配置请求头
headers = {
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
  'Content-Type': 'text/html; charset=utf-8',
  'Connection': 'close'
}
