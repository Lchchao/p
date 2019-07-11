import pymysql

db = pymysql.connect(
    host="rm-8vb7vr86oq9qk2tuhyo.mysql.zhangbei.rds.aliyuncs.com", user="work",
             password="Wjbb12345", db="stock-data", port=3306)

cur = db.cursor()



if __name__ == "__main__":
    pass