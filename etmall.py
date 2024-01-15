# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 15:24:43 2023

@author: yeh1007
"""
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
from IPython.display import Image,display
from io import BytesIO

# from PIL import Image as PILimg


import requests
from urllib.parse import urlparse, parse_qs
import pymssql

from datetime import datetime


# 創建 Edge 選項
edge_options = Options()
edge_options.use_chromium = True

# 添加禁用購物提醒的首選項
edge_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2  # 禁用通知
})

# 創建 Edge WebDriver 實例
myweb = webdriver.Edge(options=edge_options)


myweb.get("https://www.etmall.com.tw/")
win_main = myweb.window_handles[0]

time.sleep(5)
findtext = myweb.find_element(By.CSS_SELECTOR, '#txtSearchKeyword')
findtext.send_keys("電風扇")
findtext.send_keys(Keys.RETURN)

time.sleep(5)

# 设置最大滚动次数
max_scroll_count = 28
scroll_increment = 100  # 定义每次滚动的增量

for _ in range(max_scroll_count):
    myweb.execute_script("window.scrollBy(0, arguments[0]);", scroll_increment)
    time.sleep(0.5)  # 短暂等待页面加载

itemList = myweb.find_elements(By.XPATH, "//ul[contains(@class, 'n-card__list')]/li[not(@class)]")

for item in itemList:
    
    imgsrc = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
    imgurl = imgsrc.split('?')[0]
    image_data = requests.get(imgurl).content    
        
    
    nextButton = item.find_element(By.CLASS_NAME, 'n-pic')
    nextButton.click()
    win_detail = myweb.window_handles[1]
    myweb.switch_to.window(win_detail)
    time.sleep(5)
    
    
    server = 'CSCE1112002-03'
    username = 'momouser'
    password = 'M123456'
    database = '20231119'
     
    myConn = pymssql.connect(server, username, password, database) 
    myCursor = myConn.cursor()
    


    value1 = myweb.find_element(By.XPATH, "//link[@rel='canonical']").get_attribute('href').split('/')[-1]
    value2 = 'ETMALL'
    #value3 = myweb.find_element(By.XPATH, "//td[text()='商品名稱']/following-sibling::td/p").text
    value3 = myweb.find_element(By.CLASS_NAME, 'n-title--18.m-bottom-sm').text
    
    try:
        value4 = myweb.find_element(By.XPATH, "//td[text()='品牌']/following-sibling::td/p").text
    except:
        value4 = value3.split()[0] if value3 else ''
    
    try:
        #value5 = myweb.find_element(By.XPATH, "//td[contains(text(), '尺') or contains(text(), '規') or contains(text(), '容') or contains(text(), '種')]/following-sibling::td/p").text
        value5 = myweb.find_element(By.CLASS_NAME, 'table.table--bordered.table--product-detail').text
    except:
        value5 = myweb.find_element(By.ID, 'ProductSpec').text
    
    value6 = myweb.find_element(By.CLASS_NAME, 'n-price__num').text
    
    value8 = datetime.now()
    value9 = '電風扇'
    
    if not value4.strip():
        value4 = value3.split()[0] if value3 else ''
    
    print(value1, value2, value3, value4, value5, value6, value8, value9)
    display(Image(image_data))
    print('--------------------------------------------------------')

    sql = """
        INSERT INTO frommomo (id, site, productname, brandname, specification, price, photo, createdate, searchby)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

    try:
        # Execute the SQL command
        myCursor.execute(sql, (value1, value2, value3, value4, value5, value6, pymssql.Binary(image_data), value8, value9))
        # Commit your changes in the database
        myConn.commit()
    except Exception as e:
        # Rollback in case there is any error
        print(f"An error occurred: {e}")
        myConn.rollback()
        
    myConn.close()    
    
    myweb.close()
    myweb.switch_to.window(win_main)
    
myweb.close()

# Perform other actions or validations as needed

# Close the driver
#driver.quit()



