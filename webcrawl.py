'''
柏克萊新書排行榜
'''
import requests
import pymssql
 
from bs4 import BeautifulSoup as bs
 
         
myConn = pymssql.connect('CSCE1112002-03','momouser','M123456','20231119')
myConn.autocommit(True)
 
myCursor = myConn.cursor()
 
myResponse = requests.get('https://search.books.com.tw/search/query/key/%E6%8E%92%E8%A1%8C/cat/all')
myResponse.encoding = myResponse.apparent_encoding
soup = bs(myResponse.content, "html.parser")
 
page_num = (soup.find('div', attrs={'class':'search_results'}).find('p').text).split('/')[1]
def getalldata():
    sql = "delete from book "
    myCursor.execute(sql)
    titlecount = 1
    for pageNo in range(1, int(page_num)+1): #int(page_num)
        myResponse = requests.get('https://search.books.com.tw/search/query/cat/all/sort/1/v/1/spell/3/ms2/ms2_1/page/' + str(pageNo) + '/key/%E6%8E%92%E8%A1%8C')
        myResponse.encoding = myResponse.apparent_encoding
        soup = bs(myResponse.content, "html.parser")
        alltitleset = soup.find_all('div', attrs={'class':'table-td'})
        for idx in range(0, len(alltitleset)):
            mytitle = alltitleset[idx].find('a').get('title')
            print('Page ', pageNo, 'Item:' , idx+1)
            print('書名:',mytitle)
            try:
              thisauthor = alltitleset[idx].find('p', attrs={'class':'author'}).find('a').get('title')
            except:            
              thisauthor = 'Find None'
 
            print('author:', thisauthor)
 
            
            sql = "insert into book(title_id, title,author)values("
            sql += str(titlecount) + ","
            sql += "'" +mytitle + "',"
            sql += "'" + thisauthor + "')"
            print('-----')
            print(sql)
            print('-----')
            titlecount += 1
            #print(sql)
            myCursor.execute(sql)
 
#------------------------
getalldata()    
 
myCursor.close()
myConn.close()