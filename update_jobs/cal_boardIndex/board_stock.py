from config import data_path
import os




board_data = os.path.join(data_path,'industry_stock.csv')

# print(board_data)





def board_to_stock():
    board_dict = {}
    with open (board_data, 'r', encoding='utf-8') as file:
        for content in file:
            item = content.split(',')
            industry = item[6].strip('"')
            if industry not in board_dict:
                board_dict[industry] = []
            board_dict[industry].append(item[1].strip('"'))
        return board_dict










if __name__ == "__main__":
    r = board_to_stock()
    print(r)