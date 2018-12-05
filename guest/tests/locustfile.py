from locust import HttpLocust, task, TaskSet

"""对签到系统做性能测试"""


class UserBehavior(TaskSet):

    def on_start(self):
        self.login()

    def login(self):
        self.client.post('/login_action/', data={'username': 'admin', 'password': 'admin123'})

    @task(2)
    def event_manage(self):
        self.client.get('/event_manage/')

    @task(2)
    def guest_manage(self):
        self.client.get('/guest_manage/')

    @task(1)
    def search_phone(self):
        self.client.post('/search_phone/', data={'phone': '13812340112'})


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 6000
