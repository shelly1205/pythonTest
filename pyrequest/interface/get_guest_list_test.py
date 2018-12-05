import unittest
import requests
import sys
sys.path.append('../')
from db_fixture import test_data


# 测试查询嘉宾接口
class GetGuestListTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/get_guest_list/'

    def tearDown(self):
        print(self.result)

    # 发布会id为空
    def test_get_guest_list_01_eid_null(self):
        payload = {'eid': '', 'phone': '13511001100'}
        r = requests.get(self.base_url, params=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertIn('eid cannot be empty', self.result['message'])

    # 发布会id不为空，phone为空，但是发布会id不存在
    def test_get_guest_list_02_eid_not_exist_phone_null(self):
        payload = {'eid': '7', 'phone': ''}
        r = requests.get(self.base_url, params=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertIn('query result is empty', self.result['message'])

    # 发布会id不为空，phone为空，发布会id存在，查询到多个结果
    def test_get_guest_list_03_phone_null(self):
        payload = {'eid': '1', 'phone': ''}
        r = requests.get(self.base_url, params=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertIn('success', self.result['message'])

    # 发布会id不为空，phone不为空，但是发布会id不存在
    def test_get_guest_list_04_eid_not_exist(self):
        payload = {'eid': '7', 'phone': '13511001100'}
        r = requests.get(self.base_url, params=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertIn('query result is empty', self.result['message'])

    # 发布会id不为空，phone不为空，但是phone不存在
    def test_get_guest_list_05_phone_not_exist(self):
        payload = {'eid': '1', 'phone': '13511001102'}
        r = requests.get(self.base_url, params=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertIn('query result is empty', self.result['message'])

    # 发布会id不为空，phone不为空，查询到唯一结果
    def test_get_guest_list_06_phone_success(self):
        payload = {'eid': '5', 'phone': '13511001102'}
        r = requests.get(self.base_url, params=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertIn('success', self.result['message'])


if __name__ == '__main__':
    test_data.init_data()
    unittest.main()
