from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemModelTmp
        fields = (
            'companyCode',
            'itemCode',
            'barcode',
            'discountEndDttm',
            'discountPrice',
        )