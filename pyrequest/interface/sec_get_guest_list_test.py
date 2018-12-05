from Crypto.Cipher import AES
import base64
import requests
import unittest
import json


# 测试查询嘉宾接口--带AES加密算法
class AESTest(unittest.TestCase):

    def setUp(self):
        BS = 16
        # 生成补位函数
        # 因为encrypt()函数要求被加密字符串长度必须是16、24、32位，
        # 但是接口参数的个数和长度不固定，所以需要使用pad函数对长度进行处理
        self.pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

        self.base_url = 'http://127.0.0.1:8000/api/sec_get_guest_list/'
        self.app_key = 'W7v4IWH8hdjk0t9U'

    def tearDown(self):
        print(self.result)

    # AES密文太长，用base64模块中的urlsafe_b64encode()对AES密文进行二次加密，便于传输
    def encryptBase64(self, src):
        return base64.urlsafe_b64encode(src)

    # 生成AES密文
    def encryptAES(self, src, key):
        iv = b'r6Tg7u8Iuj80I6G9'
        cryptor = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cryptor.encrypt(self.pad(src))
        return self.encryptBase64(ciphertext)

    def test_aes_interface_01_request_error(self):
        payload = {'eid': 1, 'phone': '18011001100'}

        # 转化为json格式，并加密
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.get(self.base_url, data={'data': encoded})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10011)
        self.assertIn('request error', self.result['message'])

    def test_aes_interface_02_phone_error(self):
        payload = {'eid': 1, 'phone': '18011001100'}

        # 转化为json格式，并加密
        encoded = self.encryptAES(json.dumps(payload), self.app_key).decode()

        r = requests.post(self.base_url, data={'data': encoded})
        self.result = r.json()
        self.assertEqual(self.result['status'], 10022)
        self.assertIn('query result is empty', self.result['message'])


if __name__ == '__main__':
    unittest.main()
