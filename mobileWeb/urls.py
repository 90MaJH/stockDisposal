from django.urls import path
from . import views

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
    path('trade/<int:itemId>', views.trade, name='trade'),

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

    #chatting
    path('fsOe9ms1b', views.fsOe9ms1b, name='fsOe9ms1b'),
    path('fsOe9ms1b_ma', views.fsOe9ms1b_ma, name='fsOe9ms1b_ma'),
    path('ssOe9ms1b', views.ssOe9ms1b, name='ssOe9ms1b'),
    path('ssOe9ms1b_ma', views.ssOe9ms1b_ma, name='ssOe9ms1b_ma'),
    path('tsOe9ms1b', views.tsOe9ms1b, name='tsOe9ms1b'),
    path('tsOe9ms1b_ma', views.tsOe9ms1b_ma, name='tsOe9ms1b_ma'),
    path('writeChatting', views.writeChatting, name='writeChatting'),
    path('imageUploadChatting', views.imageUploadChatting, name='imageUploadChatting')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
