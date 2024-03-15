#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

if __name__ == '__main__': 
  from PyInstaller import __main__ 
  params = [
    '-F',
    '-w',
    '--noupx',
    '--clean',
    '--name=StocksFetcher',
    'src/gui/stocks_fetcher_gui.py',
    # '--add-binary={0};lib'.format(os.path.realpath('lib/ffmpeg.exe')),
    '-y',
    '--distpath=./dist'
  ]
  __main__.run(params)
