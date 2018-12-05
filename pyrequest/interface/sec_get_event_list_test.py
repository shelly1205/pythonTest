import unittest
import requests


# 查询发布会接口--带用户认证
class GetEventListTestSec(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/sec_get_event_list/'

    def tearDown(self):
        print(self.result)

    # auth为空
    def test_sec_get_event_list_01_auth_null(self):
        payload = {'eid': '1'}
        r = requests.get(self.base_url, params=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10011)
        self.assertIn('user auth null', self.result['message'])

    # auth错误
    def test_sec_get_event_list_02_auth_fail(self):
        auth_user = ('admin', 'admin')
        payload = {'eid': '1', 'name': ''}
        r = requests.get(self.base_url, auth=auth_user, params=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10012)
        self.assertIn('user auth fail', self.result['message'])

    # auth正确，eid参数为空
    def test_sec_get_event_list_03_eid_null(self):
        auth_user = ('admin', 'admin123')
        payload = {'eid': '', 'name': ''}
        r = requests.get(self.base_url, auth=auth_user, params=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10021)
        self.assertIn('parameter error', self.result['message'])


if __name__ == '__main__':
    unittest.main()
