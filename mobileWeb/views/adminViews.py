from django.shortcuts import render

from mobileWeb.forms import *
from mobileWeb.models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ipware.ip import get_ip
from datetime import datetime



@csrf_exempt
def registerMart(request):
    try:
        if request.method == 'POST':
            form = MartForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'mobileWeb/userPages/index/index.html')
        else:
            form = MartForm()
            return render(request, 'mobileWeb/admin/register_mart.html', {'form': form})
    except Exception as ex:
        print('Error occured : ', ex)

@csrf_exempt
def registerItem(request):
    try:
        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                form = ItemForm()
                return render(request, 'mobileWeb/admin/register_item.html', {'form': form})
        else:
            form = ItemForm()
            return render(request, 'mobileWeb/admin/register_item.html', {'form': form})
    except Exception as ex:
        print('Error occured : ', ex)

@csrf_exempt
def delete(request):
    try:
        marts = MartModel.objects.filter(use_yn__exact='Y').values('id', 'name', 'imageFileNo', 'xPosition',
                                                                   'yPosition')
        items = ItemModel.objects.filter(stockYn__exact='Y').filter(use_yn__exact='Y').filter(
            expirationDate__gte=datetime.now()).values('id', 'mart', 'name', 'originalPrice', 'discountPrice', 'expirationDate').order_by('mart_id',
                                                                                                           'seq')

        return render(request, 'mobileWeb/admin/delete.html', {'marts': marts, 'items': items})
    except Exception as ex:
        print('Error occured : ', ex)

@csrf_exempt
def deleteItem(request):
    try:
        item = ItemModel.objects.filter(id__exact=request.POST['item'])[0]
        item.use_yn = 'N'
        item.save()
        return HttpResponse("1")
    except Exception as ex:
        print('Error occured : ', ex)

@csrf_exempt
def deleteMart(request):
    try:
        mart = MartModel.objects.filter(id__exact=request.POST['mart'])[0]
        mart.use_yn = 'N'
        mart.save()
        return HttpResponse("1")
    except Exception as ex:
        print('Error occured : ', ex)


@csrf_exempt
def addStatistics(request):
    try:
        action = request.POST['action']
        browser = request.META['HTTP_USER_AGENT']
        ip = get_ip(request)
        statistics = StatisticsModel(action=action, browser=browser, ip=ip)
        statistics.save()
        return HttpResponse("1")
    except Exception as ex:
        print('Error occured : ', ex)

@csrf_exempt
def viewStatistics(request):
    try:
        statistics = StatisticsModel.objects.filter(action__exact='purchaseItem').order_by('-id')[:30]
        return render(request, 'mobileWeb/admin/viewStatistics.html', {'statistics':statistics})
    except Exception as ex:
        print('Error occured : ', ex)


@csrf_exempt
def test(request):
    try:
        return render(request, 'mobileWeb/admin/test.html')
    except Exception as ex:
        print('error occured ', ex)