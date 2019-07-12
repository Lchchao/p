from config import cur, db
import traceback



def get_stock_shares(code):
    shares_sql = "SELECT total_share from shares_tushare " \
                 "where ts_code = '%s' order by `index` " \
                 "desc limit 1" % code
    try:
        cur.execute(shares_sql)
        result = cur.fetchall()
        for item in result:
            return item[0]
    except Exception:
        traceback.print_exc()
        return []



def get_stock_price_change(code, date):
    if code.startswith('6'):
        table = '163_dayk_bfq_sh'
    else:
        table = '163_dayk_bfq_sz'
    stock_sql = "SELECT close, changePct from %s where code = '%s' and timestamp = '%s'" % (table, code, date)
    try:
        cur.execute(stock_sql)
        result = cur.fetchall()
        for item in result:
            print(item)
    except Exception:
        traceback.print_exc()




if __name__ == "__main__":
    # r = get_stock_shares('000001.SZ')
    r = get_stock_price_change('000001.SZ', '20190712')
    print(r)