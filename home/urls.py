from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
#from .views import *

app_name = 'home'
urlpatterns = [
        path('', views.index, name='index'),
        path('menu/', views.menu, name='menu'),
        path('<int:item_id>/', views.detail, name='detail'),
        path('<int:item_id>/results/', views.results, name='results'),
        path('<int:item_id>/purchase/', views.purchase, name='purchase'),
        path('populateFoodElf/',views.populateFoodElf,name='populateFoodElf'),
#        path('sqli/',views.sqlInjectionTutorial,name='sqlInjectionTutorial'),
#        path('showUser/',views.showUser,name='showUser'),

]
