from django.db import models
from tasks.models import Task
from robots.models import Robot
from utils.choices import Status

# Create your models here.


class Item(models.Model):
    task_id = models.ForeignKey(to=Task, null=False, blank=False,
                                on_delete=models.CASCADE, db_index=True)
    robot_id = models.ForeignKey(to=Robot, null=True, blank=True,
                                 on_delete=models.CASCADE, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    observation = models.CharField(null=True, blank=True, max_length=100)
    status = models.CharField(null=False, blank=False, max_length=50,
                              choices=Status.choices,
                              default=Status.CREATED)

    def __str__(self) -> str:
        return str(self.id)
