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
    path('selectItem', views.selectItem, name='selectItem'),
    path('addStatistics', views.addStatistics, name='addStatistics'),
    path('viewStatistics', views.viewStatistics, name='viewStatistics'),

    path('imtPosRegister', views.imtPosRegister, name='imtPosRegister'),
    path('imtPosRegisterTest', views.imtPosRegisterTest, name='imtPosRegisterTest'),
    path('imtPosSaleInfoTest', views.imtPosSaleInfoTest, name='imtPosSaleInfoTest'),
    path('imtPosSaleConfirmTest', views.imtPosSaleConfirmTest, name='imtPosSaleConfirmTest'),

    path('fsOe9ms1b', views.fsOe9ms1b, name='fsOe9ms1b'),
    path('fsOe9ms1b_ma', views.fsOe9ms1b_ma, name='fsOe9ms1b_ma'),
    path('ssOe9ms1b', views.ssOe9ms1b, name='ssOe9ms1b'),
    path('ssOe9ms1b_ma', views.ssOe9ms1b_ma, name='ssOe9ms1b_ma'),
    path('writeChatting', views.writeChatting, name='writeChatting'),
]
