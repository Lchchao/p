import os,sys
from config import data_path


import pandas as pd

boardfile = os.path.join(data_path,'index_data.csv')


# 使用简称，调用stock_price函数
def get_borad_change_interval(board, start, end):
    df_board = pd.read_csv(boardfile)
    print(df_board)
    date_list = df_board['date'].tolist()
    lines = [date_list[i] for i in range(len(date_list)) if str(date_list[i]) >= start and str(date_list[i]) <= end]
    begin = [1000.,]* len(df_board.columns[1:])
    change_list = []
    for date in lines:
        df_new = df_board.loc[df_board['date'] == date, df_board.columns[1:]]
        value = df_new.values.tolist()[0]
        index = [begin[i]*(1.+value[i]/100.) for i in range(len(value))]
        begin = index
        val = [(df_board.columns[i+1], date, value[i], begin[i]) for i in range(len(value))]
        print(val)
        change_list.append(val)
    print(change_list)
    result = []
    for number in range(len(change_list[0])):
        industry = []
        print(change_list[0][number])
        for index in range(len(change_list[number])):
            print(change_list[number][0])

    # data = [change_list[i][j] for j in range(len(change_list[0])) for i in range(len(change_list))]
    # print(data)






















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
    r = get_borad_change_interval('水务','20190601', '20190625')
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