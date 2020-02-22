from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('registerMart', views.registerMart, name='registerMart'),
    path('registerItem', views.registerItem, name='registerName'),
    path('delete', views.delete, name='delete'),
    path('deleteMart', views.deleteMart, name='deleteMart'),
    path('deleteItem', views.deleteItem, name='deleteItem'),
    path('purchaseItem', views.purchaseItem, name='purchaseItem'),
]
