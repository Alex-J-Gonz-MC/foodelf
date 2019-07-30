from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
#from .views import *

app_name = 'operationsResearch'
urlpatterns = [
        path('', views.index, name='index'),
        path('billHistory/', views.billHistory, name='billHistory'),
        
]