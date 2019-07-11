
from flask import Flask,request,abort
app = Flask(__name__)
import time
import json
from template import all_boards
import os
from srf_log import init_log

from stock_web.template import board_rank
from stock_web.template import stocks_price





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




log_path = os.path.join(CUR_PATH, './log')
if not os.path.exists(log_path):
    os.makedirs(log_path)
init_log(log_path, 'stock_web')




@app.route('/')
def route():
    return 'hello world'


@app.route('/boards_name')
def get_allboards():
    boards = all_boards.get_wande_boards3()[1]
    return build_reponse(boards, error_code=0)


@app.route('/board/change',methods=['GET'])
def board_index_change():
    start = request.args.get('start')
    end = request.args.get('end')
    data = board_rank.get_increase_states(start, end)
    return build_reponse(data, error_code=0)



@app.route('/board/stock',methods=['GET'])
def board_stock_change():
    start = request.args.get('start')
    end = request.args.get('end')
    board = request.args.get('board')
    data = stocks_price.board_stock_list(board, start, end)
    return build_reponse(data, error_code=0)






@app.route('/board/rank_days')
def get_borad_rank_days():
    pass






app.debug = True
app.run()