#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://finance.yahoo.com/quote/7003.T

import time
import random
import re
from mechanicalsoup import StatefulBrowser

from src.api import database
from src.config.env import useragents

browser = StatefulBrowser(user_agent=useragents[random.randint(0, len(useragents) - 1)])

url = 'https://finance.yahoo.com/quote/7003.T'
browser.open(url)

for tr in browser.page.select('div[id="quote-summary"] table tr'):
  key = tr.contents[0].text
  value = tr.contents[1].text
  print(key + " : " + value)