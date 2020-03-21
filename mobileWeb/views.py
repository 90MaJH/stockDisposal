from django.shortcuts import render
from .forms import *
from .models import *
from datetime import datetime, date
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

        return render(request, 'mobileWeb/index/index.html', {'marts': marts, 'items': items})
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
        return render(request, 'mobileWeb/martDetail/martDetail.html', {'mart':mart, 'items':items})
    except Exception as ex:
        print('error occured : ', ex)

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




@csrf_exempt
def fsOe9ms1b(request):
    try:
        chattingList = Chatting.objects.filter(userId__exact='0',partnerId__exact='1')\
                       |Chatting.objects.filter(userId__exact='1')

        return render(request, 'mobileWeb/chatting/fsOe9ms1b.html', {'chattingList':chattingList})
    except Exception as ex:
        print(" error occured : ", ex)

@csrf_exempt
def fsOe9ms1b_ma(request):
    try:
        chattingList = Chatting.objects.filter(userId__exact='0',partnerId__exact='1')\
                       |Chatting.objects.filter(userId__exact='1')

        return render(request, 'mobileWeb/chatting/fsOe9ms1b_ma.html', {'chattingList': chattingList})
    except Exception as ex:
        print(" error occured : ", ex)


@csrf_exempt
def ssOe9ms1b(request):
    try:
        chattingList = Chatting.objects.filter(userId__exact='0',partnerId__exact='2')\
                       |Chatting.objects.filter(userId__exact='2')

        return render(request, 'mobileWeb/chatting/ssOe9ms1b.html', {'chattingList':chattingList})
    except Exception as ex:
        print(" error occured : ", ex)

@csrf_exempt
def ssOe9ms1b_ma(request):
    try:
        chattingList = Chatting.objects.filter(userId__exact='0',partnerId__exact='2')\
                       |Chatting.objects.filter(userId__exact='2')

        return render(request, 'mobileWeb/chatting/ssOe9ms1b_ma.html', {'chattingList': chattingList})
    except Exception as ex:
        print(" error occured : ", ex)


@csrf_exempt
def tsOe9ms1b(request):
    try:
        chattingList = Chatting.objects.filter(userId__exact='0',partnerId__exact='3')\
                       |Chatting.objects.filter(userId__exact='3')

        return render(request, 'mobileWeb/chatting/tsOe9ms1b.html', {'chattingList':chattingList})
    except Exception as ex:
        print(" error occured : ", ex)

@csrf_exempt
def tsOe9ms1b_ma(request):
    try:
        chattingList = Chatting.objects.filter(userId__exact='0',partnerId__exact='3')\
                       |Chatting.objects.filter(userId__exact='3')

        return render(request, 'mobileWeb/chatting/tsOe9ms1b_ma.html', {'chattingList': chattingList})
    except Exception as ex:
        print(" error occured : ", ex)


@csrf_exempt
def writeChatting(request):
    try:
        userId = request.POST['userId']
        partnerId = request.POST['partnerId']
        message = request.POST['message']
        chatting = Chatting(userId=userId, partnerId=partnerId, message=message)
        chatting.save()
        return HttpResponse("1")
    except Exception as ex:
        print("error occured : ", ex)

@csrf_exempt
def imageUploadChatting(request):
    try:
        if request.method == 'POST':
           form = ChattingImageUploadForm(request.POST, request.FILES)
           if form.is_valid():
               form.save()
               #### ajax json 처리 참고할
               # return JsonResponse({'error': False, 'message': 'Uploaded Successfully'})
               return HttpResponse("1")
           else:
                #### ajax json 처리 참고할
                # return JsonResponse({'error': True, 'errors': form.errors})
                return HttpResponse("error")
        else:
            form = ChattingImageUploadForm()
            form.fields['userId'].widget = forms.HiddenInput()
            form.fields['partnerId'].widget = forms.HiddenInput()
            return render(request, 'mobileWeb/chatting/imageUpload.html', {'form': form})
    except Exception as ex:
        print('Error occured : ', ex)