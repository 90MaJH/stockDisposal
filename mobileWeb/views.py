from django.shortcuts import render
from .forms import *
from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ipware.ip import get_ip



# Create your views here.
@csrf_exempt
def index(request):
    try:
        marts = MartModel.objects.filter(use_yn__exact='Y').values('id', 'name', 'imageFileNo', 'xPosition',
                                                                   'yPosition')
        items = ItemModel.objects.filter(stockYn__exact='Y').filter(use_yn__exact='Y').filter(
            expirationDate__gte=datetime.now()).values('id', 'mart', 'name', 'originalPrice', 'discountPrice', 'expirationDate', 'comment').order_by('mart_id',
                                                                                                           'seq')
        browser = request.META['HTTP_USER_AGENT']
        ip = get_ip(request)
        statistics = StatisticsModel(action='openIndexPage', browser=browser, ip=ip)
        statistics.save()

        return render(request, 'mobileWeb/index/index.html', {'marts': marts, 'items': items})
    except Exception as ex:
        print('Error occured : ', ex)

@csrf_exempt
def registerMart(request):
    try:
        if request.method == 'POST':
            form = MartForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'mobileWeb/index/index.html')
        else:
            form = MartForm()
            return render(request, 'mobileWeb/admin/register_mart.html', {'form': form})
    except Exception as ex:
        print('Error occured : ', ex)

@csrf_exempt
def registerItem(request):
    try:
        if request.method == 'POST':
            form = ItemForm(request.POST)
            if form.is_valid():
                mart = form.cleaned_data['mart']
                seq = ItemModel.objects.filter(mart__exact=mart).values('seq').order_by('-seq')[:1]
                if seq:
                    seq = seq[0]['seq'] + 1
                else:
                    seq = 1
                item = ItemModel(mart=mart, seq=seq, name=form.cleaned_data['name'], originalPrice=form.cleaned_data['originalPrice'],
                                 discountPrice=form.cleaned_data['discountPrice'], expirationDate=form.cleaned_data['expirationDate'], comment=form.cleaned_data['comment'])
                item.save()
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
def purchaseItem(request):
    try:
        item = ItemModel.objects.filter(id__exact=request.POST['item'])[0]
        item.stockYn = 'N'
        item.save()
        return HttpResponse("1")
    except Exception as ex:
        print('Error occured : ', ex)

@csrf_exempt
def selectItem(request):
    try:
        item = ItemModel.objects.filter(id__exact=request.POST['item'])[0]
        if item.stockYn == 'N':
            return HttpResponse("1"); #이미 판매된 상품입니다.
        elif item.use_yn == 'N':
            return HttpResponse("2");  # 삭제된 상품입니다.
        else:
            item = item.as_json()
            return HttpResponse(json.dumps(item), content_type="application/json")

            # items = [item.as_json() for item in item]
            # return HttpResponse(json.dumps(items), content_type="application/json")
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
        statistics = StatisticsModel.objects.all().order_by('-id')[:30]
        return render(request, 'mobileWeb/admin/viewStatistics.html', {'statistics':statistics})
    except Exception as ex:
        print('Error occured : ', ex)