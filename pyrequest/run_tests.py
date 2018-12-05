import unittest
import sys
import time
import HTMLTestRunner
sys.path.append('./')
from db_fixture import test_data


test_dir = './interface'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='*_test.py')

if __name__ == '__main__':
    test_data.init_data()

    now = time.strftime('%Y-%m-%d %H-%M-%S')
    filename = './report/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           title='Guest Manage System Interface Test Report',
                                           description='运行环境：MySQL(PyMySQL), Requests, unittest '
                                           )
    runner.run(discover)
    fp.close()
