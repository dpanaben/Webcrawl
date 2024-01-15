# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 15:24:43 2023

@author: yeh1007
"""
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

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

myweb = webdriver.Edge(options=edge_options)

# Navigate to the website
myweb.get("https://www.rakuten.com.tw/")

actions = ActionChains(myweb)
actions.click().perform()

mainwin = myweb.window_handles[0]

time.sleep(5)
findtext = myweb.find_element(By.XPATH, '/html/body/div[1]/header/div[2]/div[1]/div[2]/div[2]/div[1]/form/div/input')
findtext.send_keys("電風扇")
findtext.click()
findtext.send_keys(Keys.RETURN)

time.sleep(5)

# 设置最大滚动次数
max_scroll_count = 50
scroll_increment = 100  # 定义每次滚动的增量

for _ in range(max_scroll_count):
    myweb.execute_script("window.scrollBy(0, arguments[0]);", scroll_increment)
    time.sleep(0.5)  # 短暂等待页面加载
    

itemList = myweb.find_element(By.CLASS_NAME, 'results-grid').find_elements(By.CLASS_NAME, 'product-grid__detail')

for item in itemList:
    time.sleep(1)
    imgsrc = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
    #imgurl = imgsrc.split('?')[0]
    image_data = requests.get(imgsrc).content    

    value3 = item.find_element(By.CLASS_NAME, 'product-title').text
    value6 = item.find_element(By.CLASS_NAME, 'price').text


    detailUrl = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
    newwin = myweb.switch_to.new_window('tab')
    myweb.get(detailUrl)
    
    time.sleep(5)
    
    server = 'CSCE1112002-03'
    username = 'momouser'
    password = 'M123456'
    database = '20231119'
     
    myConn = pymssql.connect(server, username, password, database) 
    myCursor = myConn.cursor()
    
    value1 = myweb.find_element(By.CLASS_NAME, 'qa-base-sku').text
    value2 = 'RAKUTEN'
    
    try:
        value4 = myweb.find_element(By.XPATH, "//dt[contains(text(), '品牌')]/following-sibling::dd").text
    except:
        value4 = value3.split()[0] if value3 else ''
    

    value5 = myweb.find_element(By.ID, 'item-detail').text
    
    
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
    
    
    myweb.close()
    myweb.switch_to.window(mainwin)
    
myweb.close()







