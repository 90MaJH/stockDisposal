from django.shortcuts import render
from .forms import *

# Create your views here.

def index(request):
    try:
        marts = MartModel.objects.all().values('id', 'name', 'imageFileNo', 'xPosition', 'yPosition')
        items = ItemModel.objects.filter(stockYn__exact='Y').values('mart', 'name', 'price', 'expirationDate').order_by('mart_id', 'seq')

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
    print(request)
    try:
        if request.method == 'POST':
            form = ItemForm(request.POST)
            if form.is_valid():
                # mart = MartModel.objects.get(id__exact=form.cleaned_data['mart'])
                mart = form.cleaned_data['mart']
                seq = ItemModel.objects.filter(mart__exact=mart).values('seq').order_by('-seq')[:1]
                if seq:
                    seq = seq[0]['seq']+1
                else:
                    seq = 1
                # form.save()
                item = ItemModel(mart=mart, seq=seq, name=form.cleaned_data['name'], price=form.cleaned_data['price'], expirationDate=form.cleaned_data['expirationDate'], stockYn=form.cleaned_data['stockYn'])
                item.save()
                form = ItemForm()
                return render(request, 'mobileWeb/admin/register_item.html', {'form':form})
        else:
            form = ItemForm()
            return render(request, 'mobileWeb/admin/register_item.html', {'form':form})
    except Exception as ex:
        print('====777 : Error occured : ', ex)