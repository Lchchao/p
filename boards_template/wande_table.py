from config import cur,db
import traceback
from boards_template.all_boards import get_wande_boards3
import datetime
from boards_template.stock_analysis.stocks_price import get_board_stocks

# 使用一次后，跳过不再使用
def insert_table():
    get_boards = get_wande_boards3()
    boards = [key for key in get_boards.values()]
    board_codes = [code['code'] + ' FLOAT(32, 4) default null' for code in boards]

    board_column = ','.join(board_codes)
    table_create = "CREATE table wande_industry (date datetime default null, %s) " % board_column

    # print(table_create)
    try:
        cur.execute(table_create)
        db.commit()
    except Exception:
        traceback.print_exc()
        db.rollback()
    return ''

# 获取2016年以来，所有交易的有效时间
def get_date_2016():
    date_table = '163_dayk_bfq_sh'
    date_sql = "select distinct timestamp from %s where timestamp >= '%s' " \
            % (date_table, '2016-01-01')
    dates = []
    try:
        cur.execute(date_sql)
        results = cur.fetchall()
        for item in results:
            date = datetime.datetime.strftime(item[0], '%Y-%m-%d')
            dates.append(date)
        # print(dates)
        return dates
    except Exception:
        traceback.print_exc()


# 先进行插入整个表，后期再进行start，end的数据选择
def board_change_date(board):
    dates = get_date_2016()[680:]
    # print(dates.index('2018-10-18'))
    codes_dict = get_wande_boards3()[1]
    code = codes_dict[board]['code']
    table = 'wande_industry'
    board_indexs = []
    board_index = 490.78
    for date in dates:
        board_change = get_board_stocks(board,date)
        board_index = round(board_index*(1+board_change[2]/100),2)
        result = list(board_change) + [board_index]
        index_insert = "insert into %s (date, %s) values ('%s','%s')" % \
                       (table, code, result[1],result[3])
        print(index_insert)
        try:
            cur.execute(index_insert)
            db.commit()
        except:
            db.rollback()




    return board_indexs







def insert_board_table():
    boards_dict = get_wande_boards3()[0]
    boards = [board for board in boards_dict.keys()]
    dates = get_date_2016()

    for date in dates:
        date_boards = []

        for board in boards[:4]:
            brief = boards_dict[board]['brief']
            board_change = get_board_stocks(brief, date)
            if board_change is None:
                continue
            board_index = 1000
            board_index = round(board_index*(1+board_change[2]/100),2)
            print(board_change, board_index)
    pass









if __name__ == "__main__":
    # get_date_2016()
    board_change_date('海运指数')
    # insert_board_table()




