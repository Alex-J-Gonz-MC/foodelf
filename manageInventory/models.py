import datetime
from django.db import models
from django.utils import timezone

class Inventory(models.Model):
    inventory_id = models.IntegerField(primary_key=True,default=0)
    name = models.CharField(max_length=50)
    units = models.IntegerField(default=0)
    safety_stock = models.IntegerField(default=0)
    price_per_unit = models.FloatField(default=0)
    date_purchased = models.DateField(auto_now_add=True)
    