from django.shortcuts import render
from .forms import *

# Create your views here.

def index(request):
    try:
        marts = MartModel.objects.all().values('id', 'name', 'imageFileNo', 'xPosition', 'yPosition')
        items = ItemModel.objects.filter(stockYn__exact='Y').values('mart_id', 'name', 'price', 'expirationDate').order_by('mart_id', 'seq')

        return render(request, 'mobileWeb/index/index.html', {'marts':marts, 'items':items})
    except Exception as ex:
        print('Error occured : ', ex)

def registerMart(request):
    try:
        if request.method == 'POST' :
            form = MartForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'mobileWeb/index/index.html')
        else :
            form = MartForm()
            return render(request, 'mobileWeb/admin/register_mart.html', {'form':form})
    except Exception as ex:
        print('Error occured : ', ex)

def registerItem(request):
    try:
        if request.method == 'POST' :
            form = ItemForm(request.POST)
            if form.is_valid():
                mart = MartModel.objects.get(id__exact=form.data['mart_id'])
                seq = ItemModel.objects.filter(mart_id__exact=mart).values('seq').order_by('-seq')[:1]
                if seq:
                    seq = seq[0]['seq']+1
                else:
                    seq = 1
                # form.save()
                item = ItemModel(mart_id=mart, seq=seq, name=form.data['name'], price=form.data['price'], expirationDate=form.data['expirationDate'], stockYn=form.data['stockYn'])
                item.save()
                form = ItemForm()
                return render(request, 'mobileWeb/admin/register_item.html', {'form':form})
        else:
            form = ItemForm()
            return render(request, 'mobileWeb/admin/register_item.html', {'form':form})
    except Exception as ex:
        print('Error occured : ', ex)