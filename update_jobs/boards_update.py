


from config import data_path
from config import db, cur
import os, traceback
from update_jobs.cal_boardIndex import board_stock
from update_jobs.cal_boardIndex import board_change




def get_board_new_date():
    file_path = os.path.join(data_path, 'index_data.csv')
    date_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for content in file:
            item = content.split(',')
            date = item[0]
            date_list.append(date)

    return date_list[-1]




def get_update_date_list(last_date):
    sql = "SELECT cal_date from trade_days where " \
          "cal_date > '%s' and is_open = 1 order by cal_date asc" % last_date
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


def update_board_change():
    last_date = get_board_new_date()
    date_list = get_update_date_list(last_date)
    board_list = board_stock.board_to_stock()[0]
    out_put = data_path + '/index_data.csv'
    with open('%s' % out_put, 'a', encoding='utf-8') as file:
        print(board_list)
        for date in date_list[:5]:
            change_line = []
            for board in board_list:
                change = board_change.board_date_change(board, date)
                print(date, board, change)
                change_line.append(str(change))
            change_str = ','.join(change_line)
            value = date + ',' + change_str + '\n'
            print(value)
            file.write(value)


if __name__ == "__main__":
    # r = get_update_date_list('20081010')
    r = update_board_change()
    print(r)