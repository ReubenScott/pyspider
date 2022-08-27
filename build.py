
import sys

if __name__ == '__main__': 
  from PyInstaller import __main__ 
  params = [
    '-F',
    '-w',
    '--noupx',
    '--clean',
    '--name=kikubon',
    'src/gui/kikubon_gui.py',
    '-y',
    '--distpath=./dist'
  ]
  __main__.run(params)
