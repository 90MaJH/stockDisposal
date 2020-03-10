from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .serializers import ItemSerializer
from .models import *
from rest_framework import permissions

class ItemView(viewsets.ModelViewSet):
    queryset = ItemModelTmp.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save()