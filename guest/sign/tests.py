# coding=utf-8
from django.test import TestCase
from sign.models import Event, Guest
from django.contrib.auth.models import User

"""测试发布会签到系统功能"""


# 测试Event和Guest模型
class ModelTest(TestCase):

    # 初始化数据，创建数据
    # Django执行setUp()时，并不会真正地向数据库表插入数据，所以，不用关心产生数据后的清理工作
    def setUp(self):
        Event.objects.create(id=1, name='oneplus 3 event', status=True, limit=200,
                             address='shenzhen', start_time='2018-10-11 14:00:01')
        Guest.objects.create(id=1, event_id=1, phone='13980703034', real_name='zhangxiaoli', sign=False)

    # 测试验证，查询创建的数据，断言数据是否正确
    def test_event_models(self):
        result = Event.objects.get(name='oneplus 3 event')
        self.assertEqual(result.address, 'shenzhen')
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='13980703034')
        self.assertEqual(result.real_name, 'zhangxiaoli')
        self.assertFalse(result.sign)


# 测试index登录首页
class IndexPageTest(TestCase):

    # 测试index视图
    def test_index_page_renders_index_template(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


# 测试登录动作
class LoginActionTest(TestCase):
    # 创建用户
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123')

    # 验证添加用户是否正确
    def test_add_user(self):
        user = User.objects.get(username='admin')
        self.assertEqual(user.email, 'admin@mail.com')

    # 登录用户名密码为空
    def test_login_action_username_password_null(self):
        test_data = {'username': '', 'password': ''}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password error', response.content)

    # 用户名密码错误
    def test_login_action_username_password_error(self):
        test_data = {'username': 'abc', 'password': 'acb123'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password error', response.content)

    # 登录成功
    def test_login_action_success(self):
        test_data = {'username': 'admin', 'password': 'admin123'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)


# 测试发布会管理
class EventManageTest(TestCase):

    # 初始化数据
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123')
        Event.objects.create(id=1, name='xiaomi5', address='shenzhen',
                             limit=100, status=1, start_time='2018-12-01 14:00:00')
        self.login_user = {'username': 'admin', 'password': 'admin123'}

    # 发布会页面
    def test_event_manage_success(self):
        self.client.post('/login_action/', data=self.login_user)
        response = self.client.get('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'xiaomi5', response.content)
        self.assertIn(b'shenzhen', response.content)

    # 发布会搜索
    def test_event_manage_search_success(self):
        self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_name/', {'name': 'xiaomi5'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'xiaomi5', response.content)
        self.assertIn(b'shenzhen', response.content)


# 测试嘉宾管理
class GuestManageTest(TestCase):

    # 初始化数据
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123')
        Event.objects.create(id=1, name='xiaomi5', address='shenzhen',
                             limit=100, status=1, start_time='2018-12-01 14:00:00')
        Guest.objects.create(id=1, real_name='alice', phone='13980703034',
                             sign=False, event_id=1, email='alice@mail.com')
        self.login_user = {'username': 'admin', 'password': 'admin123'}

    # 嘉宾页面
    def test_guest_manage_success(self):
        self.client.post('/login_action/', data=self.login_user)
        response = self.client.get('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'alice', response.content)
        self.assertIn(b'alice@mail.com', response.content)

    # 嘉宾搜索
    def test_guest_manage_search_success(self):
        self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_phone/', {'phone': '13980703034'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'alice', response.content)
        self.assertIn(b'alice@mail.com', response.content)


# 测试签到功能
class SignTest(TestCase):

    # 初始化数据
    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123')
        Event.objects.create(id=1, name='xiaomi5', address='shenzhen',
                             limit=100, status=1, start_time='2018-11-01 14:00:00')
        Event.objects.create(id=2, name='oneplus4', address='beijing',
                             limit=200, status=1, start_time='2018-12-01 14:00:00')
        Guest.objects.create(id=1, real_name='alice', phone='13980703034',
                             sign=False, event_id=1, email='alice@mail.com')
        Guest.objects.create(id=2, real_name='ella', phone='15928109641',
                             sign=True, event_id=2, email='ella@mail.com')
        self.login_user = {'username': 'admin', 'password': 'admin123'}

    # 签到初始页面
    def test_sign_index(self):
        self.client.post('/login_action/', data=self.login_user)
        response = self.client.get('/sign_index/1')
        self.assertEqual(response.status_code, 301)

    # eid为空
    def test_sign_index_eid_null(self):
        self.client.post('/login_action/', data=self.login_user)
        response = self.client.get('/sign_index/')
        self.assertEqual(response.status_code, 404)

    # 手机号为空
    def test_sign_index_action_phone_null(self):
        self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1', {'phone': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'phone error', response.content)

    # 手机号和发布会不匹配
    def test_sign_index_action_phone_or_event_id_error(self):
        self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1', data={'phone': '15928109641'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'phone or event id error', response.content)

    # 嘉宾已签到
    def test_sign_index_action_user_has_sign_in(self):
        self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/2', {'phone': '15928109641'})
        self.assertEqual(response.status_code, 301)
        self.assertIn(b'user has sign in', response.content)

    # 签到成功
    def test_sign_index_action_success(self):
        self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1', {'phone': '13980703034'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'sign in success', response.content)

