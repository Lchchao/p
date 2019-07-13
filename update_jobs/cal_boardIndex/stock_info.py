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

# 参数，均使用后边的SH，或者SZ的后缀
def get_stock_price(stock, date):
    stock_result = []
    if stock.startswith('6'):
        table = '163_dayk_bfq_sh'
    else:
        table = '163_dayk_bfq_sz'
    sql = "SELECT code, close, changePct from %s where code = '%s' " \
          "and timestamp = '%s'" % (table, stock, date)
    # print(sql)
    try:
        cur.execute(sql)
        result = cur.fetchall()
        for item in result:
            if item[2] > 15.0:
                continue
            stock_result.append(item)
            return stock_result
    except Exception:
        traceback.print_exc()


def get_stock_list_price(date, stockList):
    stock_sh = [stockList[i].split('.')[0] for i in
                range(len(stockList)) if stockList[i].startswith('6')]
    stock_price = []
    if len(stock_sh) >= 2:
        stock_sql = "SELECT code, close, changePct from 163_dayk_bfq_sh " \
                    "where timestamp = '%s' and code in %s" % (date, tuple(stock_sh))
        try:
            cur.execute(stock_sql)
            result = cur.fetchall()
            for item in result:
                # print(item)
                if item[2] > 15.0:
                    continue
                stock_price.append(item)
        except Exception:
            traceback.print_exc()
    elif len(stock_sh) == 1:
        result_sh = get_stock_price(stock_sh[0], date)
        if result_sh is not None:
            stock_price = stock_price + result_sh
    stock_sz = set(stockList) - set([stock+'.SH' for stock in stock_sh])
    stock_sz = [stock.split('.')[0] for stock in list(stock_sz)]
    if len(stock_sz) >= 2:
        sz_sql = "SELECT code, close, changePct from 163_dayk_bfq_sz " \
                    "where timestamp = '%s' and code in %s" % (date, tuple(stock_sz))
        try:
            cur.execute(sz_sql)
            result = cur.fetchall()
            for item in result:
                if item[2] > 15.0:
                    continue
                stock_price.append(item)
        except Exception:
            traceback.print_exc()
    elif len(stock_sz) == 1:
        result_sz =  get_stock_price(stock_sz[0], date)
        if result_sz is not None:
            stock_price = stock_price + result_sz
    # print(stock_price)
    return stock_price




def cal_stock_change_by_mkv(stockPrice):
    if len(stockPrice) == 0:
        return 0
    else:
        mkv_sum = 0.0
        change_sum = 0.0
        for content in stockPrice:
            code = str(content[0]).zfill(6)
            price = content[1]
            changePct = content[2]
            if code.startswith('6'):
                code_exchange = code + '.SH'
            else:
                code_exchange = code + '.SZ'
            shares = get_stock_shares(code_exchange)
            if shares is not None:
                mkv_value = shares*price
                mkv_sum = mkv_sum + mkv_value
                change_sum = change_sum + mkv_value*changePct
        if mkv_sum > 0.:
            change = change_sum / mkv_sum
            return change







if __name__ == "__main__":
    # r = get_stock_shares('000001.SZ')
    # r = get_stock_list_price('20190712',['000001.SZ', '000004.SZ','600000.SH','603993.SH'])
    stock_list = [(600000, 11.52, 1.0526), (603993, 3.85, -0.2591), (1, 14.12, 4.2836), (4, 20.67, -2.4079)]
    r = cal_stock_change_by_mkv(stock_list)
    print(r)