from django.db import models

# Create your models here.


class Process(models.Model):
    title = models.CharField(null=False, blank=False, max_length=100)
    description = models.TextField(null=True, blank=True)
    enabled = models.BooleanField(null=False, blank=False, default=True)

    def __str__(self) -> str:
        return self.title
