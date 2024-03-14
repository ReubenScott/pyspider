#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
import random
from mechanicalsoup import StatefulBrowser
from src.config.env import useragents
from src.model.FundamentalData import CompanyProfile
from src.api import database


class Kabumap:

  @classmethod
  def update_company_profile(cls, *symbol):
    # 使用 time() 函数
    start_time = time.time()
    browser = StatefulBrowser(user_agent=useragents[random.randint(0, len(useragents) - 1)])

    mapping = {
      '時価総額': 'market_cap',
      '配当利回り': 'dividend_yield',
      'PBR': 'pbr',
      'PER': 'per',
      '出来高': 'volume',
      '年初来高値': 'year_high',
      '年初来安値': 'year_low',
      '信用倍率': 'credit_multiplier',
    }

    # 企業情報
    # https://dt.kabumap.com/servlets/dt/Action?SRC=basic/base&codetext=7003
    url = 'https://dt.kabumap.com/servlets/dt/Action?SRC=basic/base&codetext={symbol}'

    for row in CompanyProfile.select(CompanyProfile.symbol).where(CompanyProfile.symbol.in_(symbol)):
      # 使用 format() 方法替换字符串
      print(url.format(symbol=row.symbol))
      browser.open(url.format(symbol=row.symbol))

      elements = [element.text for element in browser.page.select('div:is(.upperArea, .lowerArea) dl > :is(dt,dd)')]

      for i in range(0, len(elements), 2):
        key, value = elements[i], elements[i + 1]
        # 剔除掉 () 之间的内容
        key = re.sub(r"\(.*?\)", "", key)

        if key in mapping.keys():
          key = mapping[key]
          setattr(row, key, value)

      database.update(row, fields=['credit_multiplier'])

    browser.close()

    # 计算耗时
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("耗时:", elapsed_time, "秒")

