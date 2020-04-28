from django.shortcuts import render

from mobileWeb.forms import *
from mobileWeb.models import *
from django.http import HttpResponse
import json
from datetime import datetime, timedelta


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

                if barcode != '':
                    expirationDate = barcode.split(' ')[1]
                    barcode = barcode.split(' ')[0]
                    expirationMonth = nowMonth
                    expirationDay = int(expirationDate[:2])
                    expirationHour = int(expirationDate[-2:])
                else:
                    expirationDate = now + timedelta(days=1)
                    expirationMonth = nowMonth
                    expirationDay = expirationDate.day
                    expirationHour = expirationDate.hour



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

                item = ItemModelTmp.objects.filter(itemCode__exact=itemCode).values('companyCode', 'itemCode',
                                                                                    'discountPrice')[0]

                return HttpResponse("0")
        else:
            form = ImtPosSaleForm(request.POST)
            return render(request, 'mobileWeb/apiTest/imtPosSaleInfoTest.html', {'form': form})
    except Exception as ex:
        print('Error occured : ', ex)


