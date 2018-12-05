import unittest
import requests
import sys
sys.path.append('../')
from db_fixture import test_data


# 测试添加发布会
class AddEventTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/add_event/'

    def tearDown(self):
        print(self.result)

    # 所有参数为空
    def test_add_event_0_all_null(self):
        payload = {'eid': '', 'name': '', 'limit': '', 'address': '', 'start_time': ''}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertIn('parameter error', self.result['message'])

    # id已经存在
    def test_add_event_1_id_exist(self):
        payload = {'eid': 1, 'name': 'YI加手机发布会', 'limit': 300, 'address': '四川成都都江堰景区',
                   'start_time': '2019-01-09 10:01:01'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertIn('event id is already exists', self.result['message'])

    # 名称已经存在
    def test_add_event_2_name_exist(self):
        payload = {'eid': 13, 'name': '红米Pro发布会', 'limit': 300, 'address': '四川成都都江堰景区',
                   'start_time': '2019-01-09 10:01:01'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10023)
        self.assertIn('event name is already exists', self.result['message'])

    # 日期格式错误
    def test_add_event_3_time_type_error(self):
        payload = {'eid': 12, 'name': 'mac发布会', 'limit': 300, 'address': '四川成都都江堰景区',
                   'start_time': '2019 '}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10024)
        self.assertIn('start_time format error', self.result['message'])

    # status为空，添加成功
    def test_add_event_4_success(self):
        payload = {'eid': 11, 'name': 'YI加手机发布会', 'limit': 300, 'address': '四川成都都江堰景区',
                   'start_time': '2019-01-09 10:01:01'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertIn('add event success', self.result['message'])


if __name__ == '__main__':
    test_data.init_data()
    unittest.main()
