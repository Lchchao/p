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
            # print(change_list[index][number])
            industry.append(change_list[index][number])
        result.append(industry)
    for item in result:
        print(item)

    # data = [change_list[i][j] for j in range(len(change_list[0])) for i in range(len(change_list))]
    # print(data)





















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