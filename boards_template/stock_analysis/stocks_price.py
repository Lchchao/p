from config import cur
import traceback
from boards_template import all_boards
import datetime
# 所有总股本数，建立一个字典
def get_code_shares():
    share_table = 'shares_tushare'
    shares_sql = "select distinct ts_code, total_share from %s order by trade_date desc" \
            % (share_table)
    # print(shares_sql)
    shares = {}
    try:
        cur.execute(shares_sql)
        result = cur.fetchall()
        for item in result:
            code = item[0]
            code_exchange = code.split('.')[0]
            shares[code_exchange] = item[1]

        return shares
    except Exception:
        traceback.print_exc()



# 给定一个code，可以获得它的当日变化量，及当日的市值
# 市值，采用当日的价格，和当日的总股本
def get_industry_change(code, date):
    result = {}
    shares = get_code_shares()
    if code.startswith('6'):
        table = '163_dayk_bfq_sh'
    else:
        table = '163_dayk_bfq_sz'
    industry_sql = "select close, changePct from %s where code = " \
                   "'%s' and timestamp = '%s' limit 1" % (table,code, date)
    try:
        cur.execute(industry_sql)
        results = cur.fetchall()
        for item in results:
            mk_value = 0
            if code in shares.keys():
                share = shares[code]
                mk_value = round(item[0] * share/10000,4)
            values = {
                'date': date,
                'price': item[0],
                'changepct': item[1],
                'mk_value': mk_value
            }
            result[code] = values
        return result
    except Exception:
        traceback.print_exc()



# 可以依据一个board，计算出他的当日涨幅
def get_board_stocks(board, date):
    stocks = all_boards.get_wande_stock(board)
    if len(stocks) > 0:
        change_sum = 0
        mkvalues_sum = 0.0
        for stock in stocks:
            stock_func = get_industry_change(stock, date)
            # print(stock_func)
            if stock in stock_func.keys():
                values = stock_func[stock]
                if values['changepct'] is not None:
                    change_sum = change_sum + values['changepct']*values['mk_value']
                    mkvalues_sum = mkvalues_sum + values['mk_value']
        if mkvalues_sum > 0:
            change_average = round(change_sum/mkvalues_sum,4)
        # print(board, date, change_average)
            return board, date, change_average


def get_stock_date_change(start, end, stock_list):
    stock_sh = [x for x in tuple(stock_list) if x.startswith('6')]
    stock_sql_sh = "SELECT code, name, timestamp, close, `change`, changePct from 163_dayk_bfq_sh " \
                "where code in %s and timestamp between '%s' and '%s'" % \
                    (tuple(stock_sh), start, end)
    stock_sz = [x for x in tuple(stock_list) if not x.startswith('6')]
    stock_sql_sz = "SELECT code, name, timestamp, close, `change`, changePct from 163_dayk_bfq_sz " \
                "where code in %s and timestamp between '%s' and '%s'" % \
                (tuple(stock_sz), start, end)
    print(stock_sql_sh)
    print(stock_sql_sz)
    try:

        cur.execute(stock_sql_sh)
        result_sh = cur.fetchall()
        cur.execute(stock_sql_sz)
        result_sz = cur.fetchall()
        result = result_sh + result_sz
        stock_list = []
        stock_obj = {}
        stock_obj['date_list'] = []
        prev_code = ''
        for i in range(len(result)):
            item = result[i]
            if prev_code == '':
                stock_obj['code'] = item[0]
                stock_obj['name'] = item[1]
                prev_code = item[0]
            elif prev_code == item[0]:
                date_list = {
                    'date': datetime.datetime.strftime(item[2], '%Y-%m-%d'),
                    'price': item[3],
                    'change': item[4],
                    'changepc': item[5]
                }
                stock_obj['date_list'].append(date_list)
                stock_obj['price_begin'] = stock_obj['date_list'][0]['price']
                stock_obj['end_price'] = stock_obj['date_list'][-1]['price']
                stock_obj['changepct'] = round(100.*(stock_obj['date_list'][-1]['price']-
                                         stock_obj['date_list'][0]['price'])/stock_obj['date_list'][0]['price'], 2)
            else:
                stock_list.append(stock_obj)
                stock_obj = {}
                stock_obj['code'] = item[0]
                stock_obj['name'] = item[1]
                stock_obj['date_list'] = []
                prev_code = item[0]

                date_list = {
                    'date': datetime.datetime.strftime(item[2], '%Y-%m-%d'),
                    'price': item[3],
                    'change': item[4],
                    'changepc': item[5]
                }
                stock_obj['date_list'].append(date_list)
                stock_obj['price_begin'] = stock_obj['date_list'][0]['price']
                stock_obj['end_price'] = stock_obj['date_list'][-1]['price']
                stock_obj['changepct'] = round(100. * (stock_obj['date_list'][-1]['price'] -
                                                       stock_obj['date_list'][0]['price']) / stock_obj['date_list'][0][
                                                   'price'], 2)

            if i == len(result) - 1:
                stock_list.append(stock_obj)
        # for item in stock_list:
        #     print(item)
        stock_sort = sorted(stock_list, key=lambda x:x['changepct'], reverse=True)
        return stock_sort


    except Exception:
        traceback.print_exc()



# board 参数为code
def board_stock_list(board, start, end):
    board_dict = all_boards.get_wande_boards3()[0]
    print(board_dict)
    board_name = ''
    if board in board_dict:
        board_name = board_dict[board]['brief']
    stocks = all_boards.get_wande_stock(board_name)
    result = get_stock_date_change(start, end, stocks)
    return result




if __name__=="__main__":
    # r = get_board_stocks('采矿指数','2016-01-04')
    r = board_stock_list('3_886055_WI', '20190100', 'asd')
    # r = get_stock_date_change('20190610', '20190620', ('600399', '600000','000001','000002'))
    print(r)

