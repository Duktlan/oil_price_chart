#引入函示庫
import requests, json
from bs4 import BeautifulSoup
import pymysql
import time


#利用get取得資料
url="https://new.cpc.com.tw/division/mb/oil-more4.aspx"
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')
p=soup.find(summary="參考牌價表欄位").find("tbody").find_all("tr")
i=0
for tr in p:
    i+=1

# 打开数据库连接
db = pymysql.connect("localhost","root","","oil_price_chart")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute() 方法执行 SQL，如果表存在则删除
#cursor.execute("DROP TABLE IF EXISTS oil_price_chart")
# 创建表
#sql= """CREATE TABLE oil_price_chart (
        #date varchar(12) NOT NULL,
        #price float NOT NULL)"""
#cursor.execute(sql)

#利用日期排序
#sql= """SELECT * FROM `oil_price_chart` ORDER by date """
#cursor.execute(sql)

# SQL 查询语句
sql = """SELECT * FROM `oil_price_chart` 
        WHERE date < '%s'""" % (time.strftime("%Y/%m/%d", time.localtime()))
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取第一筆记录
    results = cursor.fetchone()
    #print(results[0])

except:
    print ("Error: unable to fecth data")

#計算日期相差
today=time.strftime("%Y/%m/%d", time.localtime())
today = time.mktime(time.strptime(today,'%Y/%m/%d'))
date_sql = time.mktime(time.strptime(results[0],'%Y/%m/%d'))
err_days = int((today - date_sql)/(24*60*60))
#print(err_days)
err_week=err_days/7
#print(err_week)
e=1

q=1
if err_week>=1:
    while q<i:
        if len(p[q].find_all("td")[4].text)>0:
            
            # SQL 插入语句
            sql = """INSERT INTO oil_price_chart(date,price)
                    VALUES (("%s"),("%f"))""" %\
                    (p[q].find_all("td")[0].text, float(p[q].find_all("td")[4].text))
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
                print("插入成功")
                e+=1
            except:
                # 如果发生错误则回滚
                db.rollback()
                print("插入失敗")
        else:
            print("no")
        if e>err_week:
            break
        q+=1

# 关闭数据库连接
db.close()