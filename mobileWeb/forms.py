from .models import *
from django import forms

class MartForm(forms.ModelForm):
    class Meta:
        model = MartModel
        fields = ['name', 'address', 'tell', 'phone', 'xPosition', 'yPosition', 'martInfo']

class ItemForm(forms.ModelForm):
    mart = forms.ModelChoiceField(queryset=MartModel.objects.filter(use_yn__exact='Y'), to_field_name='name')
    class Meta:
        model = ItemModel
        fields = ['mart', 'name', 'originalPrice', 'discountPrice', 'expirationDate', 'comment', 'stock', 'image']

class ImtPosRegisterForm(forms.Form):
    companyCode = forms.CharField(max_length=7)
    itemCode = forms.CharField(max_length=7)
    barcode = forms.CharField(max_length=20, required=False)
    discountEndDttm = forms.DateTimeField(required=False)
    discountPrice = forms.IntegerField(required=False)

class ImtPosSaleForm(forms.Form):
    companyCode = forms.CharField(max_length=7)
    itemCode = forms.CharField(max_length=7)

class ChattingImageUploadForm(forms.ModelForm):
    class Meta:
        model = Chatting
        fields = ['userId','partnerId','photo']

class nabiImageForm(forms.ModelForm):
    class Meta:
        model = nabiImage
        fields = ['photo']
