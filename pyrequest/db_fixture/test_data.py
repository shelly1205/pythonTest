import sys
from datetime import *


sys.path.append('../')
try:
    from db_fixture.mysql_db import DB
except ImportError:
    from db_fixture.mysql_db import DB


nowTime = datetime.now()
# 定义一个过去的时间
past_time = nowTime - timedelta(days=2)
# 定义一个将来的时间
future_time = nowTime + timedelta(days=2)

# create data
datas = {
    'sign_event': [
        {'id': 1, 'name': '红米Pro发布会', 'limit': 2000, 'status': 1, 'address': '北京会展中心', 'start_time': future_time, 'create_time': nowTime},
        {'id': 2, 'name': '可参加人数为0', 'limit': 0, 'status': 1, 'address': '北京会展中心', 'start_time': future_time, 'create_time': nowTime},
        {'id': 3, 'name': '当前状态为0关闭', 'limit': 2000, 'status': 0, 'address': '北京会展中心', 'start_time': future_time, 'create_time': nowTime},
        {'id': 4, 'name': '发布会已结束', 'limit': 2000, 'status': 1, 'address': '北京会展中心', 'start_time': past_time, 'create_time': nowTime},
        {'id': 5, 'name': '小米5发布会', 'limit': 2000, 'status': 1, 'address': '北京国家会议中心', 'start_time': future_time, 'create_time': nowTime},
    ],
    'sign_guest': [
        {'id': 1, 'real_name': 'alen', 'phone': 13511001100, 'email': 'alen@mail.com', 'sign': 0, 'event_id': 1, 'create_time': nowTime},
        {'id': 2, 'real_name': 'has sign', 'phone': 13511001101, 'email': 'sign@mail.com', 'sign': 1, 'event_id': 1, 'create_time': nowTime},
        {'id': 3, 'real_name': 'tom', 'phone': 13511001102, 'email': 'tom@mail.com', 'sign': 0, 'event_id': 5, 'create_time': nowTime},
    ],
}


def init_data():
    db = DB()
    db.init_data(datas)


if __name__ == '__main__':
    init_data()
