from django.shortcuts import render
from .forms import *
from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ipware.ip import get_ip
from datetime import datetime, timedelta




# Create your views here.
@csrf_exempt
def index(request):
    try:
        marts = MartModel.objects.filter(use_yn__exact='Y').values('id', 'name', 'imageFileNo', 'xPosition',
                                                                   'yPosition')
        items = ItemModel.objects.filter(stockYn__exact='Y').filter(use_yn__exact='Y').filter(
            expirationDate__gte=datetime.now()).filter(stock__gt=0).values('id', 'mart', 'name', 'originalPrice', 'discountPrice', 'expirationDate', 'comment', 'stock').order_by('mart_id',
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
                                 discountPrice=form.cleaned_data['discountPrice'], expirationDate=form.cleaned_data['expirationDate'],
                                 comment=form.cleaned_data['comment'], stock=form.cleaned_data['stock'])
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

def imtPosRegister(request):
    try:
        companyCode = request.POST['companyCode']
        itemCode = request.POST['itemCode']
        barcode = request.POST['barCode']
        originalPrice = int(request.POST['originalPrice'])
        discountPrice = int(request.POST['discountPrice'])

        imtPosRegisterCommon(companyCode, itemCode, barcode, originalPrice, discountPrice)

    except Exception as ex:
        print('Error occrued : ', ex)

def imtPosRegisterTest(request):
    try:
        if request.method == 'POST':
            form = ImtPosRegisterForm(request.POST)
            if form.is_valid():
                companyCode = form.cleaned_data['companyCode']
                itemCode = form.cleaned_data['itemCode']
                barcode = form.cleaned_data['barcode']
                # originalPrice = int(form.cleaned_data['originalPrice'])
                originalPrice = 5000
                discountEndDttm = form.cleaned_data['discountEndDttm']
                if form.cleaned_data['discountPrice']:
                    discountPrice = int(form.cleaned_data['discountPrice'])
                else:
                    discountPrice = 0

                # imtPosRegisterCommon(companyCode, itemCode, barcode, originalPrice, discountPrice)
                expirationDate = barcode.split(' ')[1]
                barcode = barcode.split(' ')[0]
                discountRatio = 0

                now = datetime.now()
                nowDateTime = now.strftime('%Y-%m-%d %H:%M:%S')
                nowDateTime = nowDateTime.split(' ')
                nowDate = nowDateTime[0]
                nowDate = nowDate.split('-')
                nowYear = int(nowDate[0])
                nowMonth = int(nowDate[1])
                nowDay = int(nowDate[2])
                nowTime = nowDateTime[1]
                nowTime = nowDateTime[1].split(':')
                nowHour = int(nowTime[0])

                expirationMonth = nowMonth
                expirationDay = int(expirationDate[:2])
                expirationHour = int(expirationDate[-2:])

                if discountEndDttm == None:
                    discountEndDttm = now + timedelta(days=1)

                if (expirationDay - nowDay) == 0:
                    timeGap = expirationHour - nowHour
                else:
                    timeGap = expirationHour - nowHour + 24

                if timeGap == 0:
                    discountRatio = 50
                elif timeGap == 1:
                    discountRatio = 40
                elif timeGap == 2:
                    discountRatio = 35
                elif timeGap == 3:
                    discountRatio = 30
                elif timeGap == 4:
                    discountRatio = 25
                elif timeGap == 5:
                    discountRatio = 20
                elif timeGap == 6:
                    discountRatio = 15
                else:
                    discountRatio = 10

                if discountPrice == 0:
                    discountPrice = originalPrice - (originalPrice * discountRatio / 100)

                item = ItemModelTmp(companyCode=companyCode, itemCode=itemCode, barcode=barcode, discountEndDttm=discountEndDttm, discountPrice=discountPrice)
                item.save()

                # returnJson = {
                #     'companyCode': companyCode,
                #     'itemCode': itemCode,
                #     'originalPrice': originalPrice,
                #     'discountPrice': discountPrice
                # }

                # return HttpResponse(json.dumps(returnJson), content_type="application/json")
                return HttpResponse("0")
        else:
            form = ImtPosRegisterForm()
            return render(request, 'mobileWeb/apiTest/imtPosRegisterTest.html', {'form': form})
    except Exception as ex:
        print('Error occrued : ', ex)

def imtPosRegisterCommon(companyCode, itemCode, barcode, originalPrice, discountPrice):
    try:
        expirationDate = barcode.split(' ')[1]
        barcode = barcode.split(' ')[0]
        discountRatio = 0

        now = datetime.now()
        nowDateTime = now.strftime('%Y-%m-%d %H:%M:%S')
        nowDateTime = nowDateTime.split(' ')
        nowDate = nowDateTime[0]
        nowDate = nowDate.split('-')
        nowYear = int(nowDate[0])
        nowMonth = int(nowDate[1])
        nowDay = int(nowDate[2])
        nowTime = nowDateTime[1]
        nowTime = nowDateTime[1].split(':')
        nowHour = int(nowTime[0])

        expirationMonth = nowMonth
        expirationDay = int(expirationDate[:2])
        expirationHour = int(expirationDate[-2:])

        if (expirationDay - nowDay) == 0:
            timeGap = expirationHour - nowHour
        elif (expirationDay - nowDay) == 1:
            timeGap = expirationHour - nowHour + 24

        if timeGap == 0:
            discountRatio = 50
        elif timeGap == 1:
            discountRatio = 40
        elif timeGap == 2:
            discountRatio = 35
        elif timeGap == 3:
            discountRatio = 30
        elif timeGap == 4:
            discountRatio = 25
        elif timeGap == 5:
            discountRatio = 20
        elif timeGap == 6:
            discountRatio = 15
        else:
            discountRatio = 10

        if discountPrice == 0:
            discountPrice = originalPrice - (originalPrice * discountRatio / 100)



        returnJson = {
            'companyCode': companyCode,
            'itemCode': itemCode,
            'originalPrice': originalPrice,
            'discountPrice': discountPrice
        }

        return HttpResponse(json.dumps(returnJson), content_type="application/json")
    except Exception as ex:
        print('Error occrued : ', ex)

def imtPosSaleInfoTest(request):
    try:
        if request.method == 'POST':
            form = ImtPosSaleForm(request.POST)
            if form.is_valid():
                companyCode = form.cleaned_data['companyCode']
                itemCode = form.cleaned_data['itemCode']
                barcode = form.cleaned_data['barcode']

                item = ItemModelTmp.objects.filter(itemCode__exact=itemCode).values('companyCode','itemCode','discountPrice')[0]

                return HttpResponse(json.dumps(item), content_type="application/json")
        else:
            form = ImtPosSaleForm(request.POST)
            return render(request, 'mobileWeb/apiTest/imtPosSaleInfoTest.html', {'form': form})
    except Exception as ex:
        print('Error occured : ', ex)


def imtPosSaleConfirmTest(request):
    try:
        if request.method == 'POST':
            form = ImtPosSaleForm(request.POST)
            if form.is_valid():
                companyCode = form.cleaned_data['companyCode']
                itemCode = form.cleaned_data['itemCode']
                barcode = form.cleaned_data['barcode']

                item = ItemModelTmp.objects.filter(itemCode__exact=itemCode).values('companyCode', 'itemCode',
                                                                                    'discountPrice')[0]

                return HttpResponse("0")
        else:
            form = ImtPosSaleForm(request.POST)
            return render(request, 'mobileWeb/apiTest/imtPosSaleInfoTest.html', {'form': form})
    except Exception as ex:
        print('Error occured : ', ex)