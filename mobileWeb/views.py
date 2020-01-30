from django.shortcuts import render
from .forms import *

# Create your views here.

def index(request):
    try:
        marts = MartModel.objects.all().values('id', 'name', 'address', 'tell', 'phone')
        #print("marts " , marts)
        #marts id별로 item을 담는 자료구조가 필요..뭘까?
        items = ItemModel.objects.all().values('seq', 'name', 'price', 'expirationDate')
        #print("items " , items)
        return render(request, 'mobileWeb/index/index.html', {'marts':marts, 'items':items})
    except Exception as ex:
        print('Error occured : ', ex)

def registerMart(request):
    try:
        if request.method == 'POST' :
            form = MartForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'mobileWeb/index/index.html')
        else :
            form = MartForm()
            return render(request, 'mobileWeb/admin/register_mart.html', {'form':form})
    except Exception as ex:
        print('Error occured : ', ex)

def registerItem(request):
    try:
        if request.method == 'POST' :
            form = ItemForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'mobileWeb/index/index.html')
        else:
            form = ItemForm()
            return render(request, 'mobileWeb/admin/register_item.html', {'form':form})
    except Exception as ex:
        print('Error occured : ', ex)