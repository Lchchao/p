from update_jobs.cal_boardIndex import board_stock
from update_jobs.cal_boardIndex import stock_info





def board_date_change(board, date):
    board_dict= board_stock.board_to_stock()[1]
    if board in board_dict.keys():
        stocks = board_dict[board]


    pass




def get_exchange_date():
    pass

def cal_board_list_change():
    board_list = board_stock.board_to_stock()[0]
    for board in board_list:
        print(board)


if __name__ == "__main__":
    pass
