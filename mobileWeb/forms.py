from .models import *
from django import forms

class MartForm(forms.ModelForm):
    class Meta:
        model = MartModel
        fields = ['name', 'address', 'tell', 'phone']

class ItemForm(forms.ModelForm):
    choices = MartModel.objects.all().values('id', 'name')
    marts = forms.CharField(label='select mart name', widget=forms.Select(choices=choices))
    class Meta:
        model = ItemModel
        fields = ['mart_id', 'name', 'price', 'expirationDate', 'stockYn']