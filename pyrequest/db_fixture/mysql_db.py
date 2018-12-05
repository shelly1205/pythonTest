from os.path import dirname, abspath
from pymysql import connect, cursors
from pymysql.err import OperationalError
import configparser
import datetime

# ==========读取db_config.ini文件设置============

# 获得当前文件的上级目录
base_dir = dirname(dirname(abspath(__file__)))
file_path = base_dir + '/db_config.ini'
# 读取配置文件
cf = configparser.ConfigParser()
cf.read(file_path)

# 获取配置文件中的内容
host = cf.get('mysqlconf', 'host')
port = cf.get('mysqlconf', 'port')
user = cf.get('mysqlconf', 'user')
password = cf.get('mysqlconf', 'password')
db_name = cf.get('mysqlconf', 'db_name')

# ==============封装MySQL基本操作================


class DB:
    # 连接数据库
    def __init__(self):
        try:
            self.conn = connect(host=host,
                                port=int(port),
                                user=user,
                                password=password,
                                db=db_name,
                                charset='utf8mb4',
                                cursorclass=cursors.DictCursor
                                )
        except OperationalError as e:
            print('MySQL Error:', e)

    # 清除表数据
    def clear(self, table_name):
        real_sql = 'delete from ' + table_name + ';'
        with self.conn.cursor() as cursor:
            # MySQL中设置了foreign key关联，造成无法更新或删除数据，需要禁用mysql的外键约束
            cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
            # re = cursor.execute('SELECT  @@FOREIGN_KEY_CHECKS;') # 查看FOREIGN_KEY_CHECKS的值
            # print(re)
            cursor.execute(real_sql)
        self.conn.commit()

    # 插入表数据
    def insert(self, table_name, data):
        # 对数据转化格式
        new_key = []
        for key in data:
            # 将value转化为字符型
            data[key] = "'" + str(data[key]) + "'"
            # 因为有些表中的字段(如sign_event中的limit)是mysql的保留字,所以避免发生错误，统一将key转化为`key`
            key = "`" + key + "`"
            # 将转化的key保留在新的列表中
            new_key.append(key)

        # 用join函数分别将key和value组合起来
        key = ','.join(new_key)
        value = ','.join(data.values())

        # print('key:', key)
        # print('value:', value)

        # 组合sql语句
        real_sql = 'INSERT INTO ' + table_name + '(' + key + ') VALUES(' + value + ');'
        # print(real_sql)

        # 执行sql
        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
        self.conn.commit()

    # 关闭数据库连接
    def close(self):
        self.conn.close()

    # 拆分数据表名和数据，将每条数据依次插入
    def init_data(self, datas):
        for table, data in datas.items():
            self.clear(table)
            for d in data:
                self.insert(table, d)
        self.close()


if __name__ == '__main__':
    nowTime = datetime.datetime.now()
    db = DB()
    # table_name = 'sign_event'
    # data = {'id': 12, 'name': 'HONG米', 'limit': 2000, 'status': 1, 'address': '上海市体育馆',
    #         'start_time': '2018-12-01 12:00:00', 'create_time': nowTime}
    # table_name2 = "sign_guest"
    # data2 = {'real_name': 'alen', 'phone': '12312341234', 'email': 'alen@mail.com',
    #          'sign': 0, 'event_id': 1, 'create_time': nowTime}
    #
    # db.clear(table_name)
    # db.insert(table_name, data)
    # db.clear(table_name2)
    # db.insert(table_name2, data2)
    # db.close()

    datas = {
        'sign_event': [
            {'id': 10, 'name': 'HONG米', 'limit': 2000, 'status': 1, 'address': '上海市体育馆',
             'start_time': '2018-12-01 12:00:00', 'create_time': nowTime}
        ],
        'sign_guest': [
            {'real_name': 'alen', 'phone': '12312341234', 'email': 'alen@mail.com',
             'sign': 0, 'event_id': 1, 'create_time': nowTime}
        ]
    }
    db.init_data(datas)
