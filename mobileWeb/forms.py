from .models import *
from django import forms

class MartForm(forms.ModelForm):
    class Meta:
        model = MartModel
        fields = ['name', 'address', 'tell', 'phone', 'xPosition', 'yPosition']

class ItemForm(forms.ModelForm):
    choicesQueryset = MartModel.objects.all().values('id', 'name')
    choicesDic = []
    for choice in choicesQueryset:
        choicesDic.append((choice['id'], choice['name']))
    mart_id = forms.CharField(label='mart', widget=forms.Select(choices=choicesDic))
    class Meta:
        model = ItemModel
        fields = ['mart_id', 'name', 'price', 'expirationDate', 'stockYn']