from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ItemView

item_list = ItemView.as_view({
    'post': 'create',
    'get': 'list'
})

item_detail = ItemView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_updates',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('items/', item_list, name='item_list'),
    path('items/<int:pk>/', item_detail, name='item_detail'),
])