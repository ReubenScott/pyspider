# coding=utf-8

import time
import json
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import ui as ui
from selenium.webdriver.support import expected_conditions as EC

def run():

  try:
    # 執行檔的路徑 webdriver 	  
    service = Service("D:/Application/Browser/chrome-win/chromedriver.exe")
    print(service.command_line_args())
    service.start()

    # chrome://version/， 可執行檔的路徑	
    options = webdriver.ChromeOptions()
    options.binary_location = "D:/Application/Browser/chrome-win/chrome.exe"
    # 启用带插件的浏览器 設定檔路徑 设置成用户自己的数据目录
    # options.add_argument("--user-data-dir="+r"C:/Users/tanoshi/AppData/Local/Chromium/User Data/")
    # 打开chrome浏览器
    driver = webdriver.Chrome(options=options)
  
  
    wait = ui.WebDriverWait(driver,20)
    # Step # | name | target | value
    # 1 | open | / | 
    driver.get("https://free-ss.site/")
    print(driver.title) 
    
    
    # 2 | setWindowSize | 1047x618 | 
    driver.maximize_window();
    
    odd = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='tbv2_wrapper']//tr[@class='odd']//span/i[@class='fa fa-qrcode']")))
    odd.click()      
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='qrcode' and @class='layui-layer-wrap']//a")))      
    vmess = element.get_attribute("href")  
    print(vmess)  
  
    time.sleep(10)    
    
    #鼠标点击空白区域
    ActionChains(driver).move_by_offset(0,0).click().perform();  
    
    even = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='tbv2_wrapper']//tr[@class='even']//span/i[@class='fa fa-qrcode']")))
    even.click() 
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='qrcode' and @class='layui-layer-wrap']//a")))      
    vmess = element.get_attribute("href")  
    print(vmess)  
  
    time.sleep(10)  
    
  except BaseException as msg:
    print(msg)
  finally: 
    driver.quit()
    service.stop()
    
if __name__ == '__main__':
  run()




