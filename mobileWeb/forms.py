from .models import *
from django import forms

class Mart(forms.ModelForm):
    class Meta:
        model = Mart
        fields = ['name', 'address', 'tell', 'phone']

class Item(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'expirationDate', 'stockYn']