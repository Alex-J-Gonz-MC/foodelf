from django.contrib import admin

from .models import Server, Customer, ActiveTables

admin.site.register(Server)
admin.site.register(Customer)
admin.site.register(ActiveTables)
# Register your models here.
