from django.db import models
from items.models import Item

# Create your models here.


class Value(models.Model):
    item_id = models.OneToOneField(Item, on_delete=models.CASCADE,
                                   db_index=True)

    name = models.CharField(null=True, blank=True, max_length=50,
                            default='value')
    value_number = models.DecimalField(null=True, blank=True, max_digits=20,
                                       decimal_places=2)
    value_text = models.TextField(null=True, blank=True, max_length=200)

    def __str__(self) -> str:
        return str(self.id)
