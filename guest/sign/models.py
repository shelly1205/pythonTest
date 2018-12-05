from django.db import models

# Create your models here.


# 发布会表
class Event(models.Model):
    name = models.CharField(max_length=100)  # 发布会名称
    limit = models.IntegerField()  # 限制参加人数
    status = models.BooleanField()  # 状态
    address = models.CharField(max_length=200)  # 发布会地址
    start_time = models.DateTimeField('events time')  # 发布会开始时间
    create_time = models.DateTimeField(auto_now=True)  # 创建时间，自动获取当前时间

    def __str__(self):
        return self.name


# 嘉宾表
class Guest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # 关联发布会id，一个嘉宾一定属于某一场发布会
    real_name = models.CharField(max_length=64)  # 嘉宾姓名
    phone = models.CharField(max_length=16)  # 电话
    email = models.EmailField()  # email
    sign = models.BooleanField()  # 签到状态
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("event", "phone")

    def __str__(self):
        return self.real_name
