# coding:utf-8

import os
from tkinter import StringVar, LabelFrame, Label, Entry, Button, Text, Tk  
from tkinter.constants import W, NONE, END
import tkinter.filedialog
import tkinter.messagebox

from src.media import kikubon


class KikubonGui():

  def __init__(self, init_window_name):
    self.init_window_name = init_window_name
    
    # m3u地址
    self.m3u_url = StringVar()
    
    # 保存文件路径
    self.save_forder = StringVar()
    
    # 保存文件名
    self.save_name = StringVar()
    
    # cookie
    self.cookie = StringVar()
    
  # 设置窗口
  def set_init_window(self):
    self.init_window_name.title("kikubon.jp 下载工具")
    self.init_window_name.geometry('+500+200')
    
    labelframe = LabelFrame(text="配置")
    labelframe.grid(column=0, row=0, padx=5, pady=5)
    
    Label(labelframe, text="音频的HLS信息：").grid(row=0, column=0, sticky=W)
    m3upath = Entry(labelframe, width=100, textvariable=self.m3u_url)
    m3upath.insert('0', 'https://kikubon.jp/mlist.php?asKey=4813&.m3u8')
    m3upath.grid(row=0, column=1, columnspan=2, sticky=W)
    
    Label(labelframe, text="保存目录：").grid(row=1, column=0, sticky=W)
    forder = Entry(labelframe, width=50, textvariable=self.save_forder)
    user_down_path = os.path.expanduser('~') + "/Downloads"
    forder.insert('0', user_down_path)
    forder.grid(row=1, column=1, columnspan=2, sticky=W)
    Button(labelframe, text="浏览", command=self.select_save_forder).grid(row=1, column=2, sticky=W)
    
    Label(labelframe, text="保存文件名：").grid(row=2, column=0, sticky=W)
    kikubon = Entry(labelframe, width=50, textvariable=self.save_name)
    kikubon.insert('0', 'kikubon')
    kikubon.grid(row=2, column=1, columnspan=2, sticky=W)
    
    Label(labelframe, text="Cookie：").grid(row=3, column=0, sticky=W)
    # wrap属性是指 自动换行。WORD表示单词换行；CHAR(default)表示字符换行;NONE 表示不自动换行
    self.cookie_text = Text(labelframe, width=100, height=4)
    self.cookie_text.insert('1.0', 'kikubonses=ggm3ijialp7up1van8i9lj5sim; login20160719=a4c8940220d0e0cea851043aec67f4b9e44c22c4; __c__login20160719=d41123a6e04fd28ae8a7bf2ccb6fcd22e38b2066; browsingData=["720"]; cookieconsent_status=deny')
    self.cookie_text.grid(row=3, column=1, columnspan=2, sticky=W) 
    
    downframe = LabelFrame()
    downframe.grid(row=1, column=0, padx=0, pady=0)
    
    Button(downframe, text="开始下载", command=self.download).grid(row=0, column=0)
    
    text = Text(downframe, width=100, height=10, wrap=NONE)
    text.insert('1.0', '这是文本框,你可以输入任何内容')
    text.grid(row=1, column=0, sticky=W) 
  
  # 添加目录
  def select_save_forder(self):
    # self.filename = tkinter.filedialog.askopenfilename()
    fodername = tkinter.filedialog.askdirectory()
    self.save_forder.set(fodername)
  
  # 开始下载
  def download(self):
    m3u_path = self.m3u_url.get()
    dpath = self.save_forder.get()
    
    file_name = self.save_name.get()
    
  # url, dpath, file_name, cookie
    # print("文件路径：%s\n" %(self.getFilePath))
    self.cookie = self.cookie_text.get("1.0", END)
 
    if kikubon.download_audio(m3u_path, dpath, file_name, self.cookie):
      tkinter.messagebox.showinfo('提示', '下载成功！')
    else:
      tkinter.messagebox.showinfo('提示', '下载失败！')

    
def gui_start():
  init_window = Tk()
  ui = KikubonGui(init_window)
  ui.set_init_window()
  
  init_window.mainloop()

  
gui_start()
