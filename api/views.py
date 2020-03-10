import json
from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import ItemSerializer
from .models import *
from rest_framework import permissions

class ItemView(viewsets.ModelViewSet):
    queryset = ItemModelTmp.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = ResponseSuccess()
        # return Response(json.dumps(res.json), status=status.HTTP_201_CREATED, headers=headers)
        return Response(res.json, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        serializer.save()


class ResponseSuccess:
    json = {"code":0, "message":"success"}