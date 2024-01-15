# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 20:38:38 2023

@author: yeh1007
"""

import pymssql
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

font_dirs = ['C:\\Windows\\Fonts\\']
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
for font_file in font_files:
    font_manager.fontManager.addfont(font_file)
plt.rcParams['font.family'] = "Microsoft JhengHei"

server = 'CSCE1112002-03'
username = 'momouser'
password = 'M123456'
database = '20231119'
 
myConn = pymssql.connect(server, username, password, database, charset='UTF-8') 

sql1 = "select brandname, avg(cast(replace(price, ',', '') as int)) as avg_price from [20231119].dbo.frommomo group by brandname order by brandname"
sql2 = "select brandname, count(productname) total from [20231119].dbo.frommomo group by brandname order by brandname"

myCursor1 = myConn.cursor()
myCursor1.execute(sql1)
data_avg = myCursor1.fetchall()
myCursor1.close()

myCursor2 = myConn.cursor()
myCursor2.execute(sql2)
data_count = myCursor2.fetchall()
myCursor2.close()

myConn.close()


brands_avg = [row[0] for row in data_avg]
avgprice = [row[1] for row in data_avg]

brands_count = [row[0] for row in data_count]
count = [row[1] for row in data_count]



# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(20, 5))

width = 0.35

import numpy as np
ind = np.arange(len(brands_avg))

# Plotting average price
ax1.bar(ind - width/2, avgprice, width, color='b', label='Average Price')
ax1.set_xlabel('Brand')
ax1.set_ylabel('Average Price', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.set_xticks(ind)
ax1.set_xticklabels(brands_avg, rotation=80)

# Instantiate a second axes that shares the same x-axis
ax2 = ax1.twinx()  
ax2.bar(ind + width/2, count, width, color='r', label='Count')
ax2.set_ylabel('Count', color='r')
ax2.tick_params(axis='y', labelcolor='r')


# Title of the plot
plt.title('Average Price and Count by Brand')

plt.show()

# brands_avg = [row[0] for row in data_avg]
# avgprice = [row[1] for row in data_avg]
# plt.bar(brands_avg, avgprice, color='b')
# plt.xlabel('Brand')
# plt.xticks(rotation=80)
# plt.ylabel('Average', color='b')
# plt.title('Average Price by Brand')
# fig = plt.gcf()
# fig.set_size_inches(15, 5)
# plt.show()

# brands_count = [row[0] for row in data_count]
# count = [row[1] for row in data_count]
# plt.bar(brands_count, count, color='r')
# plt.xlabel('Brand')
# plt.xticks(rotation=80)
# plt.ylabel('Count', color='r')
# plt.yticks(range(min(count), max(count)+1))
# plt.title('Count by Brand')
# fig = plt.gcf()
# fig.set_size_inches(15, 5)
# plt.show()