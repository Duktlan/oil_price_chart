import requests, json
from bs4 import BeautifulSoup
import pymysql
import time


url="https://new.cpc.com.tw/division/mb/oil-more4.aspx"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')
p=soup.find(summary="參考牌價表欄位").find("tbody").find_all("tr")
i=0
for tr in p:
    i+=1


db = pymysql.connect("localhost","root","","oil_price_chart")
cursor = db.cursor()
sql = """SELECT * FROM `oil_price_chart` 
        WHERE date < '%s'""" % (time.strftime("%Y/%m/%d", time.localtime()))
try:
    cursor.execute(sql)
    results = cursor.fetchone()
except:
    print ("Error: unable to fecth data")


today=time.strftime("%Y/%m/%d", time.localtime())
today = time.mktime(time.strptime(today,'%Y/%m/%d'))
date_sql = time.mktime(time.strptime(results[0],'%Y/%m/%d'))
err_days = int((today - date_sql)/(24*60*60))
err_week=err_days/7
e=1

q=1
if err_week>=1:
    while q<i:
        if len(p[q].find_all("td")[4].text)>0:
            sql = """INSERT INTO oil_price_chart(date,price)
                    VALUES (("%s"),("%f"))""" %\
                    (p[q].find_all("td")[0].text, float(p[q].find_all("td")[4].text))
            try:
                cursor.execute(sql)
                db.commit()
                print("插入成功")
                e+=1
            except:
                db.rollback()
                print("插入失敗")
        else:
            print("no")
        if e>err_week:
            break
        q+=1
db.close()
