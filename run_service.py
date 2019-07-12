from board_api import app
import os
from config import CUR_PATH





app.debug = True
app.run()



log_path = os.path.join(CUR_PATH, './log')
if not os.path.exists(log_path):
    os.makedirs(log_path)
# init_log(log_path, 'stock_web')
