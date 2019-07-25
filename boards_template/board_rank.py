import os,sys
from config import data_path


import pandas as pd

boardfile = os.path.join(data_path,'index_data.csv')


# 使用简称，调用stock_price函数
def get_borad_change_interval(start, end):
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
        val = [(df_board.columns[i+1], date, round(value[i],4), round(begin[i], 4)) for i in range(len(value))]
        change_list.append(val)

    result = []
    for number in range(len(change_list[0])):
        industry = []
        for index in range(len(change_list)):
            industry.append(change_list[index][number])
        result.append(industry)

    industry_list = []
    for item in result:
        indu_dict = {}
        indu_dict['name'] = item[0][0]
        indu_dict['start'] = str(item[0][1])
        indu_dict['end'] = str(item[-1][1])
        indu_dict['index'] = item[-1][-1]
        # indu_dict['data_list'] = [
        #     {'date': str(item[i][1]),
        #      'changepct': item[i][2],
        #      'day_index': item[i][3]
        #      }
        #     for i in range(len(item))
        # ]
        industry_list.append(indu_dict)

    indu_sort = sorted(industry_list, key=lambda x: x['index'], reverse=True)
    for num in range(len(indu_sort)):
        indu_sort[num]['id_rank'] = num+1

    return indu_sort

















if __name__ == "__main__":
    r = get_borad_change_interval('20190601', '20190625')
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