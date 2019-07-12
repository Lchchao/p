
import traceback
from config import cur


# 获取所有的板块代码，名称和简称
# 所有文件的入口都以文件的代码为映射关系
# 同时，也会给一个中文名称到，代码的映射关系

def get_wande_boards3():
    wande_industry = 'wande_industry_exp'
    boards_sql = "select code_name, brief, nodes from %s where type = 3"\
        % wande_industry
    # print(boards_sql)
    boards = {}
    briefs = {}
    try:
        cur.execute(boards_sql)
        results = cur.fetchall()
        for item in results:
            code = item[0]
            brief = item[1] + '指数'
            name = item[2]
            names = {}
            names['code'] = code
            names['key'] = name
            briefs[brief] = names

            codes = {}
            codes['name'] = name
            codes['brief'] = brief
            boards[code] = codes

        return boards, briefs
        # 返回的顺序是code为key， 中文指数为key
    except Exception:
        traceback.print_exc()



### 参数使用index_code，不适用文字描述，把code给添加到连接里边。
#### ///计算每一只板块都含有哪些股票，参数是中文指数
def get_wande_stock(board):
    boards = get_wande_boards3()[1]
    stocks = []
    if board in boards.keys():
        industry = boards[board]['key'].replace('行业','')
        board_sql = "select code, name from wande_industry_size where wind_ind_3 = '%s'" % industry
        try:
            cur.execute(board_sql)
            results = cur.fetchall()
            for item in results:
                stocks.append(item[0].split('.')[0])
            return stocks
        except Exception:
            traceback.print_exc()



if __name__=='__main__':
    r = get_wande_stock('商业银行指数')
    print(r)

