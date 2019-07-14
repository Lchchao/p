from update_jobs.cal_boardIndex import board_stock
from update_jobs.cal_boardIndex import stock_info
from config import db, cur, data_path
import traceback, os



def board_date_change(board, date):
    board_dict= board_stock.board_to_stock()[1]
    if board in board_dict.keys():
        stocks = board_dict[board]
        stock_price = stock_info.get_stock_list_price(date, stocks)
        change = stock_info.cal_stock_change_by_mkv(stock_price)
        board_change = round(change, 6)
        return board_change




def get_exchange_date():
    sql = "SELECT cal_date from trade_days where " \
          "is_open = 1 order by cal_date asc"
    trade_date = []
    try:
        cur.execute(sql)
        result = cur.fetchall()
        for item in result:
            date = item[0].strftime('%Y%m%d')
            trade_date.append(date)
        return trade_date
    except Exception:
        traceback.print_exc()




def cal_board_list_change():
    date_list = get_exchange_date()
    board_list = board_stock.board_to_stock()[0]
    out_put = data_path + '/index_data.csv'
    with open('%s' % out_put, 'a', encoding='utf-8') as file:
        file.write('%s\n' % ','.join(board_list))
        print(board_list)
        for date in date_list[:5]:
            change_line = []
            for board in board_list:
                print(date, board)
                board_change = board_date_change(board, date)
                change_line.append(str(board_change))
            board_change = ','.join(change_line)
            value = date + ',' + board_change + '\n'
            print(value)
            file.write(value)



if __name__ == "__main__":
    # r = board_date_change('制药', '19910110')
    r = cal_board_list_change()
    print(r)
