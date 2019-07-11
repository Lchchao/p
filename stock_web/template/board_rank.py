import os,sys

CUR_PATH = os.path.dirname(os.path.abspath(__file__))

root_path = os.path.split(CUR_PATH)[0] + '/../'
sys.path.append(os.path.join(root_path))



from stock_web.template import all_boards
from stock_web.template import stocks_price
import pandas as pd
import datetime, time


# 使用简称，调用stock_price函数
def get_borad_change_date(board, days=0):
    date_now = datetime.datetime.now()
    date_str = datetime.datetime.strftime(date_now, '%Y-%m-%d')
    date_begin = date_now - datetime.timedelta(days=days)
    begin_str = datetime.datetime.strftime(date_begin, '%Y-%m-%d')
    date_index = pd.date_range(begin_str, date_str)
    date_list = [pd.Timestamp(x).strftime("%Y-%m-%d") for x in date_index.values]
    print(date_list)
    filename = (CUR_PATH + '/../data/%s.txt' % board)
    file_read = open(filename, 'r', encoding='utf-8')
    date_read_list = []
    for content in file_read:
        item = content.split(',')
        date_read = item[1]
        date_read_list.append(date_read)
    for day in date_list:
        print(board, day)
        if day in date_read_list:
            continue
        board_msg = stocks_price.get_board_stocks(board,day)
        if board_msg is not None:
            print(board_msg)
            board,date,changepct = board_msg
            print(board_msg)
            file_wirite = open(filename, 'a', encoding='utf-8')
            file_wirite.write('%s,%s,%s\n' % (board, date, changepct))

# 新建立，每个文件
def get_all_borads():
    boards = all_boards.get_wande_boards3()[1]
    print(boards)
    for board_name in boards.keys():
        filename = (CUR_PATH + '/../data/%s.txt' % board_name)
        file = open(filename, 'a', encoding='utf-8')
        file.close()




def get_increase_states(start, end):
    boards = all_boards.get_wande_boards3()[1]
    index_list = []
    for board_name, board_value in boards.items():
        index_code = board_value['code']
        # print(board_name)
        filename = (CUR_PATH + '/../data/%s.txt' % board_name)
        file = open(filename, 'r', encoding='utf-8')
        stock_index = []
        for content in file:
            item = content.split(',')
            stock_index.append(
                {
                    'index_name': item[0],
                    'date': item[1],
                    'changepct': float(item[2].strip())
                }
            )
        index_sort = sorted(stock_index, key=lambda x:x['date'], reverse=False)
        date_func = lambda x: '%s-%s-%s' % (x[:4], x[4:6], x[6:8])
        num_begin = 0
        date_list = []
        for item_data in index_sort:
            date = item_data['date']
            change_begin = 1000.0
            if date >= date_func(start) and date<= date_func(end):
                if float(item_data['changepct']) > 0:
                    num_begin += 1
                change_index = change_begin*(1 + float(item_data['changepct'])/100.0)
                date_list.append(
                    {
                        'date': item_data['date'],
                        'changepct': item_data['changepct'],
                        'index_data': round(change_index,2)
                    }
                )

        if len(date_list) > 0:
            index_list.append(
                {
                    'name': board_name,
                    'index_code': index_code,
                    'index': date_list[-1]['index_data'],
                    'day_up': round(num_begin/len(date_list),2),
                    'url': 'http://127.0.0.1:5000/board/stock?board=%s&start=%s&end=%s' % (index_code, start, end),
                    'date_index':date_list,

                }
            )


    result = sorted(index_list, key=lambda x:x['index'], reverse=True)

    return result





if __name__ == "__main__":

    log_path = os.path.join(CUR_PATH, '../data')
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    r = get_increase_states('20190401', '20190625')
    print(r)










    # boards = all_boards.get_wande_boards3()[1]
    # for board_name in boards.keys():
    #     print(board_name)
    #     filename = (CUR_PATH + '/../data/%s.txt' % board_name)
    #     file = open(filename, 'a', encoding='utf-8')
    #
    #     r = get_borad_change_date(board_name, days=360)
    #     # r = get_all_borads()
    #     print(r)