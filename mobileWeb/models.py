from django.db import models

# Create your models here.


class MartModel(models.Model):
    name = models.CharField(max_length=20, blank=False)
    address = models.TextField(blank=False)
    tell = models.CharField(blank=True, max_length=12)
    phone = models.CharField(blank=True, max_length=11)
    delete_yn = models.CharField(blank=False, default="N", max_length=1)
    ins_dttm = models.DateTimeField(blank=False, auto_now_add=True)
    ins_user = models.CharField(blank=False, max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(blank=False, auto_now=True)
    upt_user = models.CharField(blank=False, max_length=20, default='ADMIN')

class ItemModel(models.Model):
    mart_id = models.ForeignKey('martModel', models.DO_NOTHING)
    seq = models.IntegerField(blank=False)
    name = models.CharField(blank=False, max_length=20)
    price = models.IntegerField(blank=False)
    expirationDate = models.DateField(blank=False)
    stockYn = models.CharField(blank=False, max_length=1, default='Y')
    delete_yn = models.CharField(blank=False, default="N", max_length=1)
    ins_dttm = models.DateTimeField(blank=False, auto_now_add=True)
    ins_user = models.CharField(blank=False, max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(blank=False, auto_now=True)
    upt_user = models.CharField(blank=False, max_length=20, default='ADMIN')

    class Meta:
        unique_together = (
            ('mart_id', 'seq')
        )
