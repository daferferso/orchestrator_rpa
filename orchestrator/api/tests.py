from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from robots.models import Robot
from processes.models import Process
from tasks.models import Task
from items.models import Item
from values.models import Value
from utils.choices import StatusRobot

# Create your tests here.


def setUp_Test_Case(self):
    self.factory = APIRequestFactory()
    self.user = User.objects.create_user(
        username='testuser', password='testpassword')
    self.token = Token.objects.create(user=self.user)
    self.process = Process.objects.create(title='testprocess')
    self.robot = Robot.objects.create(user_id=self.user,
                                      ip_address='0.0.0.0',
                                      platform='OTHER',
                                      status=StatusRobot.ACTIVE)
    self.task = Task.objects.create(
        user_id=self.user, process_id=self.process, robot_id=self.robot)
    self.item = Item.objects.create(task_id=self.task)
    self.value = Value.objects.create(item_id=self.item, value_number=10)
