from django.shortcuts import render
from .forms import *
from datetime import datetime
from django.http import HttpResponse


# Create your views here.

def index(request):
    try:
        marts = MartModel.objects.filter(use_yn__exact='Y').values('id', 'name', 'imageFileNo', 'xPosition',
                                                                   'yPosition')
        items = ItemModel.objects.filter(stockYn__exact='Y').filter(use_yn__exact='Y').filter(
            expirationDate__gte=datetime.now()).values('mart', 'name', 'price', 'expirationDate').order_by('mart_id',
                                                                                                           'seq')

        return render(request, 'mobileWeb/index/index.html', {'marts': marts, 'items': items})
    except Exception as ex:
        print('Error occured : ', ex)


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
                item = ItemModel(mart=mart, seq=seq, name=form.cleaned_data['name'], price=form.cleaned_data['price'],
                                 expirationDate=form.cleaned_data['expirationDate'])
                item.save()
                form = ItemForm()
                return render(request, 'mobileWeb/admin/register_item.html', {'form': form})
        else:
            form = ItemForm()
            return render(request, 'mobileWeb/admin/register_item.html', {'form': form})
    except Exception as ex:
        print('Error occured : ', ex)


def delete(request):
    try:
        marts = MartModel.objects.filter(use_yn__exact='Y').values('id', 'name', 'imageFileNo', 'xPosition',
                                                                   'yPosition')
        items = ItemModel.objects.filter(stockYn__exact='Y').filter(use_yn__exact='Y').filter(
            expirationDate__gte=datetime.now()).values('id', 'mart', 'name', 'price', 'expirationDate').order_by('mart_id',
                                                                                                           'seq')

        return render(request, 'mobileWeb/admin/delete.html', {'marts': marts, 'items': items})
    except Exception as ex:
        print('Error occured : ', ex)


def deleteItem(request):
    try:
        item = ItemModel.objects.filter(id__exact=request.POST['item'])[0]
        item.use_yn = 'N'
        item.save()
        return HttpResponse("1")
    except Exception as ex:
        print('Error occured : ', ex)


def deleteMart(request):
    try:
        mart = MartModel.objects.filter(id__exact=request.POST['mart'])[0]
        mart.use_yn = 'N'
        mart.save()
        return HttpResponse("1")
    except Exception as ex:
        print('Error occured : ', ex)
