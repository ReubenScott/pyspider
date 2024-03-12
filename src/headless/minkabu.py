#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
import random
from mechanicalsoup import StatefulBrowser
from src.config.env import useragents
from src.model.FundamentalData import CompanyProfile
from src.api import database


class Minkabu:

  @classmethod
  def update_company_profile(cls, *symbol):
    # 使用 time() 函数
    start_time = time.time()
    browser = StatefulBrowser(user_agent=useragents[random.randint(0, len(useragents) - 1)])

    mapping = {
      '上場市場': 'exchange',
      '上場年月日': 'listing_date',
      '単元株数': 'per_unit'
    }

    # 企業情報
    # https://minkabu.jp/stock/7003/fundamental
    url = 'https://minkabu.jp/stock/{symbol}/fundamental'

    for row in CompanyProfile.select(CompanyProfile.symbol).where(CompanyProfile.symbol.in_(symbol)):
      # 使用 format() 方法替换字符串
      print(url.format(symbol=row.symbol))
      browser.open(url.format(symbol=row.symbol))

      # browser.page.select('div[class="ly_content_wrapper"] dl[class="md_dataList"]')

      # 株式（上場市場）の状況
      stock_listed_market_status = browser.page.select('div[class="ly_content_wrapper"] dl[class="md_dataList"]')[1].text

      matches = re.findall(r"(\S+.*?)\n+", stock_listed_market_status)
      key = matches[0]
      value = matches[1]
      if key in mapping.keys():
        key = mapping[key]
        setattr(row, key, value)

      key = matches[2]
      value = matches[3]
      if key in mapping.keys():
        key = mapping[key]
        setattr(row, key, value)

      key = matches[4]
      value = matches[5]
      if key in mapping.keys():
        key = mapping[key]
        setattr(row, key, value)

      database.update(row, fields=['listing_date']);

    browser.close()

    # 计算耗时
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("耗时:", elapsed_time, "秒")

