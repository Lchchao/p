from update_jobs.cal_boardIndex.stock_info import get_stock_list_price
from update_jobs.cal_boardIndex.board_stock import board_to_stock




# 判断，start，end是否是交易日
def stock_change_in_board(board, start, end):
    board_dict = board_to_stock()
    stocklist = board_dict[board]
    stock_start = get_stock_list_price(start, stocklist)
    stock_end = get_stock_list_price(end, stocklist)

    print(stock_start)
    print(stock_end)
    stock_list = []
    for num in range(len(stock_start)):
        stock = {}
        stock['code'] = stock_start[num][0]
        stock['name'] = stock_start[num][1]
        stock['price_start'] = stock_start[num][2]
        stock['price_end'] = stock_end[num][2]
        stock['changepct'] = round((stock_end[num][2] - stock_start[num][2])/stock_start[num][2], 4)
        stock_list.append(stock)

    stock_sort = sorted(stock_list, key=lambda x: x['changepct'], reverse=True)
    return stock_sort











if __name__ == "__main__":
    # stock_list = ['000001.SZ', '002142.SZ', '002807.SZ']
    # r = get_stock_list_price('20190725', stock_list)
    r = stock_change_in_board('饮料', '20190701', '20190725')
    print(r)
