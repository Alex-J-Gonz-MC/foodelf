import datetime
from django.db import models
from django.utils import timezone
from manageTables.models import Server
# Create your models here.

class BillHistory(models.Model):
    server = models.ForeignKey(Server,on_delete=models.CASCADE)
    customers = models.CharField(max_length=200)
    items = models.CharField(max_length=200)
    date = models.DateTimeField('Date')
    time_seated = models.IntegerField(default=0)