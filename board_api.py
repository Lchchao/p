import time
import json
import os
from boards_template import board_rank, all_boards
from boards_template.stock_analysis import stocks_price
from boards_template import board_has_stocks

from flask import Flask, request, render_template

app = Flask(__name__)


CUR_PATH = os.path.dirname(os.path.abspath(__file__))

error_code_message = {
    0: '成功',
    10001:'登录失败',
    20500:'内部错误',
    20404:'接口url错误',
    30001:'接口传参错误',

}


def build_reponse(data, error_code=0):
    success = True
    if error_code is not None and error_code != 0:
        success = False
    response = {
        'sussess': success,
        'error_code': str(error_code),
        'error_message':error_code_message[error_code],
        'time':str(int(time.time()*1000)),
        'data': data

    }
    return json.dumps(response)







@app.route('/')
def route():
    return render_template('index.html')








@app.route('/boards_name')
def get_allboards():
    boards = all_boards.get_wande_boards3()[1]
    return build_reponse(boards, error_code=0)


@app.route('/boardlist',methods=['GET'])
def board_index_change():
    start = request.args.get('start')
    end = request.args.get('end')
    data = board_rank.get_borad_change_interval(start, end)
    return build_reponse(data, error_code=0)



@app.route('/boardlist/board',methods=['GET'])
def board_stock_change():
    start = request.args.get('start')
    end = request.args.get('end')
    board = request.args.get('board')
    data = board_has_stocks.stock_change_in_board(board, start, end)
    return build_reponse(data, error_code=0)



@app.route('/board/rank_days')
def get_borad_rank_days():
    pass



