import unittest
import requests
import sys
import time
import hashlib
sys.path.append('../')
from db_fixture import test_data


# 测试添加发布会,添加数字签名
class AddEventTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/sec_add_event/'
        # app_key
        self.app_key = '&Guest-Manager'

        # 当前时间
        now_time = time.time()
        self.client_time = str(now_time).split('.')[0]

        # sign
        md5 = hashlib.md5()
        sign_str = self.client_time + self.app_key
        sign_bytes_utf8 = sign_str.encode(encoding='utf-8')
        md5.update(sign_bytes_utf8)
        self.sign_md5 = md5.hexdigest()

    def tearDown(self):
        print(self.result)

    # 请求方法错误
    def test_add_event_0_request_error(self):
        payload = {'eid': '', 'name': '', 'limit': '', 'address': '', 'start_time': '', 'time': '', 'sign': ''}
        r = requests.get(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10011)
        self.assertIn('request error', self.result['message'])

    # 时间和签名参数为空
    def test_add_event_1_sign_null(self):
        payload = {'eid': '', 'name': '', 'limit': '', 'address': '', 'start_time': '', 'time': '', 'sign': ''}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10012)
        self.assertIn('user sign null', self.result['message'])

    # 请求超时
    def test_add_event_2_sign_timeout(self):
        now_time = str(int(self.client_time) - 61)
        payload = {'eid': 13, 'name': '红米Pro发布会', 'limit': 300, 'address': '四川成都都江堰景区',
                   'start_time': '2019-01-09 10:01:01', 'time': now_time, 'sign': self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10013)
        self.assertIn('user sign timeout', self.result['message'])

    # 签名错误
    def test_add_event_3_sign_error(self):
        payload = {'eid': 12, 'name': 'mac发布会', 'limit': 300, 'address': '四川成都都江堰景区',
                   'start_time': '2019 ', 'time': self.client_time, 'sign': 'abc'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10014)
        self.assertIn('user sign fail', self.result['message'])

    # 添加成功
    def test_add_event_4_sign_success(self):
        payload = {'eid': 44, 'name': 'YI加发布会', 'limit': 300, 'address': '四川成都都江堰景区',
                   'start_time': '2019-01-09 10:01:01', 'time': self.client_time, 'sign': self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertIn('add event success', self.result['message'])


if __name__ == '__main__':
    test_data.init_data()
    unittest.main()
