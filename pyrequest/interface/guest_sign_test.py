import unittest
import requests
import sys
sys.path.append('../')
from db_fixture import test_data


# 测试嘉宾签到接口
class GuestSignTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/guest_sign/'

    def tearDown(self):
        print(self.result)

    # 发布会id和phone为空
    def test_guest_sign_01_eid_phone_null(self):
        payload = {'eid': '', 'phone': ''}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertIn('parameter error', self.result['message'])

    # 发布会id不为空，phone为空
    def test_guest_sign_02_phone_null(self):
        payload = {'eid': '7', 'phone': ''}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertIn('parameter error', self.result['message'])

    # 发布会id为空，phone不为空
    def test_guest_sign_03_eid_null(self):
        payload = {'eid': '1', 'phone': ''}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertIn('parameter error', self.result['message'])

    # 发布会id不为空，phone不为空，但是发布会id不存在
    def test_guest_sign_04_eid_not_exist(self):
        payload = {'eid': '7', 'phone': '13511001100'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertIn('event id null', self.result['message'])

    # 发布会id不为空，phone不为空，但是phone不存在
    def test_guest_sign_05_phone_not_exist(self):
        payload = {'eid': '1', 'phone': '13980703034'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10025)
        self.assertIn('guest phone null', self.result['message'])

    # 发布会id存在，phone存在，但是该phone不与该发布会关联
    def test_guest_sign_06_phone_not_in_eid(self):
        payload = {'eid': '1', 'phone': '13511001102'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10026)
        self.assertIn('guest did not participate in the conference', self.result['message'])

    # 发布会id存在，phone存在，但是发布会已开始
    def test_guest_sign_07_event_has_started(self):
        payload = {'eid': '4', 'phone': '13980703034'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10024)
        self.assertIn('event has started', self.result['message'])

    # 发布会id存在，phone存在，但是发布会已禁用
    def test_guest_sign_08_event_not_available(self):
        payload = {'eid': '3', 'phone': '13980703034'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10023)
        self.assertIn('event is not available', self.result['message'])

    # 发布会id存在，phone存在，但是嘉宾已签到
    def test_guest_sign_09_guest_has_sign_in(self):
        payload = {'eid': '1', 'phone': '13511001101'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10027)
        self.assertIn('guest has sign in', self.result['message'])

    # 发布会id存在，phone存在，签到成功
    def test_guest_sign_10_success(self):
        payload = {'eid': '5', 'phone': '13511001102'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertIn('sign success', self.result['message'])


if __name__ == '__main__':
    test_data.init_data()
    unittest.main()
