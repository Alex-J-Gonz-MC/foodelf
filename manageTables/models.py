import datetime
from django.db import models
from django.utils import timezone
#from home.models import Choice
# Create your models here.

class Server(models.Model):
    name = models.CharField(max_length=200) # waiter's/waitress' name
    tables = models.IntegerField(default=0) # should hold how many tables a waiter served in a day
    tips = models.FloatField(default=0) # should hold how many tips a waiter accumulated throughout the day
    def __str__(self):
        return self.name    
class ActiveTables(models.Model):
    tableNumber = models.SmallIntegerField(default=0)
    server = models.ForeignKey(Server,on_delete=models.CASCADE)
    time = models.DateTimeField('Time Sat')
    ACCESS = models.CharField(max_length=8)
    def _str__(self):
        return self.tableNumber    
class Customer(models.Model):
    table = models.ForeignKey(ActiveTables,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    