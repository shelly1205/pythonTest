import sys
import unittest
import requests
sys.path.append('../')
from db_fixture import test_data


# 测试添加嘉宾
class GuestAddTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/add_guest/'

    def tearDown(self):
        print(self.result)

    # 所有参数都为空
    def test_add_guest_01_all_null(self):
        payload = {'real_name': '', 'phone': '', 'email': '', 'eid': ''}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertIn('parameter error', self.result['message'])

    # event_id不存在
    def test_add_guest_02_event_id_not_exist(self):
        payload = {'real_name': 'zhangxiaoli', 'phone': '13980703034',
                   'email': 'zhang@mail.com', 'eid': '7'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertIn('event id null', self.result['message'])

    # event未启用，status=0
    def test_add_guest_03_event_status_not_available(self):
        payload = {'real_name': 'zhangxiaoli', 'phone': '13980703034',
                   'email': 'zhang@mail.com', 'eid': '3'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10023)
        self.assertIn('event status is not available', self.result['message'])

    # event已满员
    def test_add_guest_04_event_number_is_full(self):
        payload = {'real_name': 'zhangxiaoli', 'phone': '13980703034',
                   'email': 'zhang@mail.com', 'eid': '2'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10024)
        self.assertIn('event number is full', self.result['message'])

    # event已开始，start_time<=now_time
    def test_add_guest_05_event_has_started(self):
        payload = {'real_name': 'zhangxiaoli', 'phone': '13980703034',
                   'email': 'zhang@mail.com', 'eid': '4'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10025)
        self.assertIn('event has started', self.result['message'])

    # 同一个event_id，phone已存在
    def test_add_guest_06_phone_repeat(self):
        payload = {'real_name': 'zhangxiaoli', 'phone': '13511001100',
                   'email': 'zhang@mail.com', 'eid': '1'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10026)
        self.assertIn('guest phone number repeat', self.result['message'])

    # 添加成功
    def test_add_guest_07_success(self):
        payload = {'real_name': 'zhangxiaoli', 'phone': '15928109641',
                   'email': 'zhang@mail.com', 'eid': '5'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertIn('add guest success', self.result['message'])


if __name__ == '__main__':
    test_data.init_data()
    unittest.main()
