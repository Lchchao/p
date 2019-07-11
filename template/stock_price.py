import pymysql
import datetime
import traceback
import numpy as np

db = pymysql.connect(host="rm-8vb7vr86oq9qk2tuhyo.mysql.zhangbei.rds.aliyuncs.com", user="work",
                                 password="Wjbb12345", db="stock-data", port=3306)
cursor = db.cursor()


def date_interval_stockprice(date_interval, code):
    now_time = datetime.datetime.now()
    now_date = datetime.datetime.strftime(now_time, '%Y-%m-%d'+' 23:59:59')
    date_interval = datetime.timedelta(days=int(date_interval))
    date_before = datetime.datetime.strftime((now_time-date_interval), '%Y-%m-%d'+' 00:00:00')
    if code.startswith('6'):
        code_database = '163_dayk_bfq_sh'
    else:
        code_database = '163_dayk_bfq_sz'
    select_sql = "select name,close,timestamp from %s where code = '%s' and timestamp between '%s' and '%s'" \
                % (code_database, code, date_before, now_date)
    # print(select_sql)
    stockprice = {}
    try:
        price_distrib = []
        cursor.execute(select_sql)
        results = cursor.fetchall()
        name = ''
        for item in results:
            name = item[0]
            price = item[1]
            date = datetime.datetime.strftime(item[2], '%Y/%m%d')
            stockprice[date] = price
            price_distrib.append(price)
        print(name, code)

        print(price_distrib)

        price_25 = round(np.percentile(price_distrib, 25),2)
        price_50 = round(np.percentile(price_distrib, 50),2)
        price_75 = round(np.percentile(price_distrib, 75),2)
        print(min(price_distrib), price_25, price_50, price_75, max(price_distrib))




    except Exception:
        traceback.print_exc()







if __name__ =='__main__':
    date_interval_stockprice(30, '603993')



