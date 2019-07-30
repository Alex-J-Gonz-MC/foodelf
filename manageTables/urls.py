from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
#from .views import *

app_name = 'manageTables'
urlpatterns = [
        path('', views.index, name='index'),
        path('<int:table_id>/', views.summary, name='summary'),
        path('<int:table_id>/menu/', views.sendToMenu, name='sendToMenu'),
        path('<int:table_id>/<int:item_id>/addItemToBill/', views.addItemToBill, name='addItemToBill'),
        path('createTable/', views.createTable, name='createTable'),
        path('<int:table_id>/closeoutTable/', views.closeoutTable, name='closeoutTable'),
        path('<int:table_id>/splitBills/', views.splitBills, name='splitBills'),
        path('updateQueue/',views.updateQueue,name='updateQueue'),
        path('inputToTable/',views.inputToTable,name='inputToTable'),
        path('updateCustomers/',views.updateCustomers,name='updateCustomers'),
        path('assignChoices/',views.assignChoices,name='assignChoices'),
        path('lobby/<str:access_code>',views.lobby,name='lobby'),
        path('getAccessCode/<str:customer_id>',views.getAccessCode,name='getAccessCode'),
        path('getBill/<str:access_code>',views.getBill,name='getBill'),
        path('showBill/<int:userID>',views.showBill,name='showBill'),
        path('personalizedMenu/',views.personalizedMenu,name='personalizedMenu'),
        path('getIngredients/',views.getIngredients,name='getIngredients'),
        
        
        
        
        
        #path('menu/', views.menu, name='menu'),
]