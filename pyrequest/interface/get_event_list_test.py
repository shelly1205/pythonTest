import unittest
import requests
import sys
sys.path.append('../')
from db_fixture import test_data


# 测试查询发布会接口
class GetEventListTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/get_event_list/'

    def tearDown(self):
        print(self.result)

    # 发布会id和name为空
    def test_get_event_list_01_all_null(self):
        payload = {'eid': '', 'name': ''}
        r = requests.get(self.base_url, params=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertIn('parameter error', self.result['message'])

    # 根据发布会id查询，但是结果不存在
    def test_get_event_list_02_id_not_exist(self):
        payload = {'eid': '7'}
        r = requests.get(self.base_url, params=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertIn('query result is empty', self.result['message'])

    # 根本发布会name查询，但是结果不存在
    def test_get_event_list_03_name_not_exist(self):
        payload = {'name': '话剧李茶的姑妈'}
        r = requests.get(self.base_url, params=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertIn('query result is empty', self.result['message'])

    # 根据发布会id搜索到结果
    def test_get_event_list_04_id_sucess(self):
        payload = {'eid': '1', 'name': ''}
        r = requests.get(self.base_url, params=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertIn('success', self.result['message'])

    # 根据发布会name搜索到结果
    def test_get_event_list_05_name_success(self):
        payload = {'eid': '', 'name': '小米5发布会'}
        r = requests.get(self.base_url, params=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertIn('success', self.result['message'])


if __name__ == '__main__':
    test_data.init_data()
    unittest.main()
