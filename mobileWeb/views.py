from django.shortcuts import render
from .forms import *

# Create your views here.

def index(request):
    try:
        return render(request, 'mobileWeb/index/index.html')
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