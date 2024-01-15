# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
from IPython.display import Image,display
from io import BytesIO

from PIL import Image as PILimg


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

myweb.get("https://www.momoshop.com.tw/")
mainwin = myweb.window_handles[0]

time.sleep(5)
findtext = myweb.find_element(By.CSS_SELECTOR, '.inputArea.ac_input.ui-autocomplete-input')
findtext.click()
findtext.send_keys("電風扇")
findtext.send_keys(Keys.RETURN)

time.sleep(5)

# 设置最大滚动次数
max_scroll_count = 15
scroll_increment = 100  # 定义每次滚动的增量

for _ in range(max_scroll_count):
    myweb.execute_script("window.scrollBy(0, arguments[0]);", scroll_increment)
    time.sleep(0.5)  # 短暂等待页面加载

itemList = myweb.find_elements(By.CLASS_NAME, 'listArea')[0].find_elements(By.TAG_NAME, 'li')

for item in itemList:
    
    detailUrl = item.find_element(By.CLASS_NAME, 'goodsUrl').get_attribute('href')
    newwin = myweb.switch_to.new_window('tab')
    myweb.get(detailUrl)
        
    time.sleep(5)
    myweb.refresh()

    myweb.find_element(By.CSS_SELECTOR, "#productForm > div.prdwarp > ul > li:nth-child(3) > span").click()
    
    server = 'CSCE1112002-03'
    username = 'momouser'
    password = 'M123456'
    database = '20231119'
     
    myConn = pymssql.connect(server, username, password, database) 
    myCursor = myConn.cursor()
    
    image_path = myweb.find_element(By.XPATH, "//img[@class='jqzoom']").get_attribute('src')
    image_data = requests.get(image_path).content
    
    webpimage = PILimg.open(BytesIO(image_data))
    png_buffer = BytesIO()
    webpimage.save(png_buffer, format="PNG")
    pngimage = png_buffer.getvalue()


    value1 = parse_qs(urlparse(detailUrl).query).get("i_code", [None])[0]
    value2 = 'MOMOSHOP'
    value3 = myweb.find_element(By.ID, 'osmGoodsName').text
    value4 = myweb.find_element(By.XPATH, "//th[contains(text(), '品牌名稱')]/following-sibling::td").text
    value5 = myweb.find_element(By.XPATH, "//th[contains(text(), '規') or contains(text(), '格') or contains(text(), '尺')]/following-sibling::td").text
    value6 = myweb.find_element(By.XPATH, "//span[@class='seoPrice']").text
    
    value8 = datetime.now()
    value9 = parse_qs(urlparse(detailUrl).query).get("kw", [None])[0]
    
    if not value4.strip():
        value4 = value3.split()[0] if value3 else ''
        
        
    print(value1, value2, value3, value4, value5, value6, value8, value9)
    display(Image(pngimage))
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
    
    time.sleep(2)
    myweb.close()
    myweb.switch_to.window(mainwin)
    
myweb.close()
    

# Perform other actions or validations as needed

# Close the driver
#driver.quit()



