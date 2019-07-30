from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'manageInventory'
urlpatterns = [
        path('', views.inventoryMain, name='inventoryMain'),
        path('prefForm/', views.preferencesForm, name='preferencesForm'),
        path('outputForm/', views.prefOut, name='prefOut'),
        path('testComms/', views.testComms, name='testComms'),
        path('testJSON/', views.testJSON, name='testJSON'),
        path('testPOST/', views.testPOST, name='testPOST'),
        path('populateForm/', views.populateForm, name='populateForm'),
        path('editInventory/<int:ingred_id>', views.editInventory, name='editInventory'),
        path('getAddStockForm/', views.getAddStockForm, name='getAddStockForm'),
        path('addStock/<int:ingred_id>', views.addStock, name='addStock'),        
        
        
        
]