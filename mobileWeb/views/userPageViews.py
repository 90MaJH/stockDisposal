import requests
from django.shortcuts import render

from mobileWeb.models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ipware.ip import get_ip
from datetime import datetime, timedelta



# Create your views here.
@csrf_exempt
def index(request):
    try:
        endDttm = datetime.now()
        startDttm = endDttm - timedelta(days=1)

        marts = MartModel.objects.filter(use_yn__exact='Y').prefetch_related('martcomment_set')
        for mart in marts:
            mart.martcomment = mart.martcomment_set.filter(ins_dttm__range=[startDttm, endDttm])
        items = ItemModel.objects.filter(stockYn__exact='Y').filter(use_yn__exact='Y').filter(
            expirationDate__gte=datetime.now()).filter(stock__gt=0).values('id', 'mart', 'name', 'originalPrice', 'discountPrice', 'expirationDate', 'comment', 'stock').order_by('mart_id')
        browser = request.META['HTTP_USER_AGENT']
        ip = get_ip(request)
        statistics = StatisticsModel(action='openIndexPage', browser=browser, ip=ip)
        statistics.save()

        return render(request, 'mobileWeb/userPages/index/index.html', {'marts': marts, 'items': items})
    except Exception as ex:
        print('Error occured : ', ex)

@csrf_exempt
def addComment(request):
    try:
        mart = MartModel.objects.get(id__exact=request.POST['martId'])
        comment = request.POST['comment']
        martComment = MartComment(mart=mart, comment=comment)
        martComment.save()
        return HttpResponse("1")
    except Exception as ex:
        print('Error occured : ', ex)

@csrf_exempt
def martDetail(request, martId):
    try:
        mart = MartModel.objects.filter(id__exact=martId).prefetch_related('itemmodel_set')[0]
        items = mart.itemmodel_set.filter(stockYn__exact='Y').filter(use_yn__exact='Y').filter(
            expirationDate__gte=datetime.now()).filter(stock__gt=0)
        return render(request, 'mobileWeb/userPages/martDetail/martDetail.html', {'mart':mart, 'items':items})
    except Exception as ex:
        print('error occured : ', ex)


@csrf_exempt
def purchaseItem(request):
    try:
        item = ItemModel.objects.filter(id__exact=request.POST['item'])[0]
        item.stock -= 1
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

