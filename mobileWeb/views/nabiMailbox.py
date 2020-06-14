import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from mobileWeb.forms import *
from mobileWeb.models import *
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from ipware.ip import get_ip


# user
def nabiMailbox(request):
    try:
        return render(request, 'mobileWeb/nabiMailbox/main.html')
    except Exception as ex:
        print('error occured : ', ex)


def child1(request):
    try:
        return render(request, 'mobileWeb/nabiMailbox/child1.html')
    except Exception as ex:
        print('error occured : ', ex)


def imageUpload(request):
    try:
        if request.method == 'POST':
            form = nabiImageForm(request.POST, request.FILES)
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
            form = nabiImageForm()
            return render(request, 'mobileWeb/nabiMailbox/main.html', {'form': form})
    except Exception as ex:
        print("error occured : ", ex)
