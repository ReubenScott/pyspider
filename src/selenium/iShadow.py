# coding=utf-8

import time
import json
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

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
    #options.add_argument("--user-data-dir="+r"C:/Users/tanoshi/AppData/Local/Chromium/User Data/")
    #options.add_argument("--headless")    
    # 打开chrome浏览器
    driver = webdriver.Chrome(options=options)
  
    wait = ui.WebDriverWait(driver,20)
    # Step # | name | target | value
    # 1 | open | / | 
    driver.get("http://www.aastocks.com/")
    print(driver.title) 
    # 2 | setWindowSize | 1047x618 | 
    #driver.set_window_size(1047, 618)
    driver.maximize_window();
    
    # 3 | click | css=.btn:nth-child(3) | 
    fss = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='intro']/div/div/div/div/a")))
    time.sleep(5)    
    fss.click() 
    #driver.find_elements_by_link_text("Get Free SS").click()  
    
    # 4 | click | css=.type > li:nth-child(3) > a | 
    #wait.until(lambda driver: driver.find_elements_by_css_selector(".type > li:nth-child(3) > a"))
    #wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='portfolio']//ol[@class='type']/li/a[@data-filter='.v2']")))
    #wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@id='portfolio']//ol[@class='type']/li/a[@data-filter='.v2']")))  
    datafilter = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='portfolio']//ol[@class='type']/li/a[@data-filter='.v2']")))  
    time.sleep(5)    
    datafilter.click()
    time.sleep(10)    
    driver.execute_script("window.scrollTo(0,2700);")
    time.sleep(5)    
        
    vnds = ('urlv203','urlv202','urlv201')
    for vnd in vnds:
      print(vnd)
      #抓取文字 vmess:// 
      vmess=driver.find_element_by_xpath("//span[@id='%s' and @class='copybtn']" %vnd).get_attribute("data-clipboard-text")  
      print(vmess)
    
      time.sleep(1)      
      #定位到要悬停的元素
      move = driver.find_element_by_xpath("//span[@id='%s' and @class='copybtn']/.." %vnd)         
      #对定位到的元素执行悬停操作
      ActionChains(driver).move_to_element(move).perform()
      time.sleep(1)  
      
      # 5 | click | linkText=Click to view QR Code | 
      qrcode = wait.until(EC.element_to_be_clickable((By.XPATH,"//span[@id='%s' and @class='copybtn']/../../h4[2]/a" %vnd)))
      qrcode.click()
      time.sleep(10)    
      
      #鼠标点击关闭
      bclose = wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@class='nivo-lightbox-close' and @title='Close']")))  
      bclose.click()
  except  Exception as e:
    print(e);    
  finally: 
    driver.quit()
    service.stop()
    
if __name__ == '__main__':
  run()

