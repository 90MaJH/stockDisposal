from django.db import models

# Create your models here.




#####tmp#####
class ItemModelTmp(models.Model):
    companyCode = models.CharField(blank=False, default='C0012', max_length=7)
    itemCode = models.CharField(blank=False, default='0001', max_length=7)
    barcode = models.CharField(blank=False, default='123213 2823', max_length=20)
    discountEndDttm = models.DateTimeField(blank=True, default='2020-03-28 23:00:00')
    discountPrice = models.FloatField(blank=True)