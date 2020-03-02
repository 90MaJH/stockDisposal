from .models import *
from django import forms

class MartForm(forms.ModelForm):
    class Meta:
        model = MartModel
        fields = ['name', 'address', 'tell', 'phone', 'xPosition', 'yPosition']

# class ItemForm(forms.ModelForm):
#     choicesQueryset = MartModel.objects.all().values('id', 'name')
#     choicesDic = []
#     for choice in choicesQueryset:
#         choicesDic.append((choice['id'], choice['name']))
#     mart_id = forms.CharField(label='mart', widget=forms.Select(choices=choicesDic))
#     class Meta:
#         model = ItemModel
#         fields = ['mart_id', 'name', 'price', 'expirationDate', 'stockYn']

class ItemForm(forms.ModelForm):
    mart = forms.ModelChoiceField(queryset=MartModel.objects.filter(use_yn__exact='Y'), to_field_name='name')
    # choiceDic = [('Y', '판매중'), ('N', '판매완료')]
    # stockYn = forms.CharField(label='stockYn', widget=forms.Select(choices=choiceDic))
    class Meta:
        model = ItemModel
        fields = ['mart', 'name', 'originalPrice', 'discountPrice', 'expirationDate', 'comment']
        # fields = ['mart', 'name', 'price', 'expirationDate', 'stockYn']

class ImtPosRegisterForm(forms.Form):
    companyCode = forms.CharField(max_length=7)
    itemCode = forms.CharField(max_length=7)
    barcode = forms.CharField(max_length=20)
    originalPrice = forms.IntegerField()
    discountPrice = forms.IntegerField(required=False)
