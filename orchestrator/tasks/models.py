from django.db import models
from django.contrib.auth.models import User
from processes.models import Process
from robots.models import Robot
from utils.choices import Status

# Create your models here.


class Task(models.Model):
    user_id = models.ForeignKey(to=User, null=False, blank=False,
                                on_delete=models.CASCADE, db_index=True)
    process_id = models.ForeignKey(to=Process, null=False, blank=False,
                                   on_delete=models.CASCADE, db_index=True)
    robot_id = models.ForeignKey(to=Robot, null=True, blank=True, default=None,
                                 on_delete=models.CASCADE,  db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(null=False, blank=False, max_length=50,
                              choices=Status.choices,
                              default=Status.CREATED)

    def __str__(self) -> str:
        return str(self.id)
