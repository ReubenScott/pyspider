
import sys

if __name__ == '__main__': 
  from PyInstaller import __main__ 
  params = [
    '-F',
    '-w',
    '--noupx',
    '--clean',
    '--name=kikubon',
    'gui/kikubon_gui.py',
    '-y'
  ]
  __main__.run(params)
