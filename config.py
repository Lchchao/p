import pymysql
import os



db = pymysql.connect(
    host="rm-8vb7vr86oq9qk2tuhyo.mysql.zhangbei.rds.aliyuncs.com", user="work",
             password="Wjbb12345", db="stock-data", port=3306)

cur = db.cursor()





CUR_PATH = os.path.realpath(__file__)
base_path = os.path.split(CUR_PATH)[0]



data_path = os.path.join(base_path, 'data')



if __name__ == "__main__":
    pass