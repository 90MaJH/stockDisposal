from django.shortcuts import render

# Create your views here.

def index(request):
    try:
        return render(request, 'mobileWeb/index/index.html')
    except Exception as ex:
        print('Error occured : ', ex)