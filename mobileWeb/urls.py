from django.urls import path
from . import views
from mobileWeb.views import *

from django.conf.urls.static import static
from django.conf.urls import include, url
from django.conf import settings

urlpatterns = [

    path('', views.index, name='index'),

    path('index', views.index, name='index'),
    path('addComment', views.addComment, name='addComment'),


    # users
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('accounts/', include('allauth.urls')),
    path('oauth', views.oauth, name='oauth'),

    path('martDetail/<int:martId>', views.martDetail, name='martDetail'),

    path('registerMart', views.registerMart, name='registerMart'),
    path('registerItem', views.registerItem, name='registerName'),
    path('delete', views.delete, name='delete'),
    path('deleteMart', views.deleteMart, name='deleteMart'),
    path('deleteItem', views.deleteItem, name='deleteItem'),

    path('purchaseItem', views.purchaseItem, name='purchaseItem'),
    path('selectItem', views.selectItem, name='selectItem'),
    path('addStatistics', views.addStatistics, name='addStatistics'),
    path('viewStatistics', views.viewStatistics, name='viewStatistics'),

    #api
    path('imtPosRegister', views.imtPosRegister, name='imtPosRegister'),
    path('imtPosRegisterTest', views.imtPosRegisterTest, name='imtPosRegisterTest'),
    path('imtPosSaleInfoTest', views.imtPosSaleInfoTest, name='imtPosSaleInfoTest'),
    path('imtPosSaleConfirmTest', views.imtPosSaleConfirmTest, name='imtPosSaleConfirmTest'),

    #test
    # path('test', views.test, name='test'),

    #mailBox
    path('nabiMailbox', views.nabiMailbox, name='nabiMailbox'),
    path('child1', views.child1, name='child1'),
    path('child2', views.child2, name='child2'),
    path('child3', views.child3, name='child3'),
    path('child1_2', views.child1_2, name='child1_2'),
    path('child2_2', views.child2_2, name='child2_2'),
    path('child3_2', views.child3_2, name='child3_2'),
    path('child1_3', views.child1_3, name='child1_3'),
    path('child2_3', views.child2_3, name='child2_3'),
    path('child3_3', views.child3_3, name='child3_3'),
    path('memoLetter', views.memoLetter, name='memoLetter'),

    path('imageUpload', views.imageUpload, name='imageUpload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
