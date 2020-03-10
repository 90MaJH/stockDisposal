from django.db import models

# Create your models here.




#####tmp#####
class ItemModelTmp(models.Model):
    companyCode = models.CharField(blank=False, default='C0012', max_length=7)
    itemCode = models.CharField(blank=False, default='0001', max_length=7)
    barcode = models.CharField(blank=True, null=True, max_length=20)
    discountEndDttm = models.DateTimeField(null=True)
    discountPrice = models.FloatField(null=True)