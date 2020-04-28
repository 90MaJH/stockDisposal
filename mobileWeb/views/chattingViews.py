from django.shortcuts import render

from mobileWeb.forms import *
from mobileWeb.models import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def fsOe9ms1b(request):
    try:
        chattingList = (Chatting.objects.filter(userId__exact='0',partnerId__exact='1')\
                       |Chatting.objects.filter(userId__exact='1'))[:20]

        return render(request, 'mobileWeb/chatting/fsOe9ms1b.html', {'chattingList':chattingList})
    except Exception as ex:
        print(" error occured : ", ex)

@csrf_exempt
def fsOe9ms1b_ma(request):
    try:
        chattingList = (Chatting.objects.filter(userId__exact='0',partnerId__exact='1')\
                       |Chatting.objects.filter(userId__exact='1'))[:20]


        return render(request, 'mobileWeb/chatting/fsOe9ms1b_ma.html', {'chattingList': chattingList})
    except Exception as ex:
        print(" error occured : ", ex)


@csrf_exempt
def ssOe9ms1b(request):
    try:
        chattingList = (Chatting.objects.filter(userId__exact='0',partnerId__exact='2')\
                       |Chatting.objects.filter(userId__exact='2'))[:20]


        return render(request, 'mobileWeb/chatting/ssOe9ms1b.html', {'chattingList':chattingList})
    except Exception as ex:
        print(" error occured : ", ex)

@csrf_exempt
def ssOe9ms1b_ma(request):
    try:
        chattingList = (Chatting.objects.filter(userId__exact='0',partnerId__exact='2')\
                       |Chatting.objects.filter(userId__exact='2'))[:20]


        return render(request, 'mobileWeb/chatting/ssOe9ms1b_ma.html', {'chattingList': chattingList})
    except Exception as ex:
        print(" error occured : ", ex)


@csrf_exempt
def tsOe9ms1b(request):
    try:
        chattingList = (Chatting.objects.filter(userId__exact='0',partnerId__exact='3')\
                       |Chatting.objects.filter(userId__exact='3'))[:20]


        return render(request, 'mobileWeb/chatting/tsOe9ms1b.html', {'chattingList':chattingList})
    except Exception as ex:
        print(" error occured : ", ex)

@csrf_exempt
def tsOe9ms1b_ma(request):
    try:
        chattingList = (Chatting.objects.filter(userId__exact='0',partnerId__exact='3')\
                       |Chatting.objects.filter(userId__exact='3'))[:20]


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
        print("error occured : ", ex)