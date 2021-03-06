from django.db import models
from django.conf import settings
from pytz import timezone

# Create your models here.



class MartModel(models.Model):
    name = models.CharField(max_length=20, blank=False)
    address = models.TextField(blank=False)
    tell = models.CharField(blank=True, max_length=12)
    phone = models.CharField(blank=True, max_length=11)
    imageFileNo = models.CharField(blank=True, max_length=3)
    xPosition = models.FloatField(blank=False)
    yPosition = models.FloatField(blank=False)
    martInfo = models.CharField(blank=True, max_length=200)
    use_yn = models.CharField(blank=False, default="Y", max_length=1)
    ins_dttm = models.DateTimeField(blank=False, auto_now_add=True)
    ins_user = models.CharField(blank=False, max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(blank=False, auto_now=True)
    upt_user = models.CharField(blank=False, max_length=20, default='ADMIN')

    def __str__(self):
        return self.name

    def as_json(self):
        return dict(
            id=self.id,
            name=self.name)

class MartComment(models.Model):
    mart = models.ForeignKey('martModel', models.DO_NOTHING)
    comment = models.CharField(blank=False, max_length=50)
    ins_dttm = models.DateTimeField(blank=False, auto_now_add=True)
    ins_user = models.CharField(blank=False, max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(blank=False, auto_now=True)
    upt_user = models.CharField(blank=False, max_length=20, default='ADMIN')

    def as_json(self):
        return dict(
            mart=self.mart.as_json(),
            comment=self.comment
            )

class ItemModel(models.Model):
    mart = models.ForeignKey('martModel', models.DO_NOTHING)
    name = models.CharField(blank=False, max_length=30)
    originalPrice = models.IntegerField(blank=False, default=0)
    discountPrice = models.IntegerField(blank=False, default=0)
    expirationDate = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(blank=False, max_length=200, default='')
    image = models.ImageField(blank=True, null=True, upload_to="images/items")
    stock = models.IntegerField(blank=False, default=1)
    stockYn = models.CharField(blank=False, max_length=1, default='Y')
    use_yn = models.CharField(blank=False, default="Y", max_length=1)
    ins_dttm = models.DateTimeField(blank=False, auto_now_add=True)
    ins_user = models.CharField(blank=False, max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(blank=False, auto_now=True)
    upt_user = models.CharField(blank=False, max_length=20, default='ADMIN')

    def as_json(self):
        return dict(
            mart=self.mart.as_json(),
            id=self.id,
            name=self.name)

    @property
    def created_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)
        return self.created_at.astimezone(korean_timezone)

class StatisticsModel(models.Model):
    action = models.CharField(blank=False, max_length=20, default='default')
    browser = models.CharField(blank=False, max_length=50, default='default')
    ip = models.CharField(blank=False, max_length=15, default='000.000.000.000')
    ins_dttm = models.DateTimeField(blank=False, auto_now_add=True)
    ins_user = models.CharField(blank=False, max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(blank=False, auto_now=True)
    upt_user = models.CharField(blank=False, max_length=20, default='ADMIN')



##trade Models
class trHeaderModel(models.Model):
    date = models.DateField(blank=False, auto_now_add=True)
    receipt_no = models.IntegerField(blank=False, default=1)
    price = models.IntegerField(blank=False, default=1)
    userEmail = models.CharField(blank=False, default='default', max_length=200)
    ins_dttm = models.DateTimeField(blank=False, auto_now_add=True)
    ins_user = models.CharField(blank=False, max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(blank=False, auto_now=True)
    upt_user = models.CharField(blank=False, max_length=20, default='ADMIN')
    # mart = models.ForeignKey('martModel', models.DO_NOTHING)
    # item = models.ForeignKey('ItemModel', models.DO_NOTHING)

class trItemModel(models.Model):
    date = models.DateField(blank=False, auto_now_add=True)
    receipt_no = models.IntegerField(blank=False, default=1)
    trHeader = models.ForeignKey('trHeaderModel', models.DO_NOTHING)
    seq = models.IntegerField(blank=False, default=1)
    mart = models.ForeignKey('martModel', models.DO_NOTHING)
    item = models.ForeignKey('itemModel', models.DO_NOTHING)
    amount = models.IntegerField(blank=False, default=1)
    unitPrice = models.IntegerField(blank=False, default=1)
    totalPrice = models.IntegerField(blank=False, default=1)
    ins_dttm = models.DateTimeField(blank=False, auto_now_add=True)
    ins_user = models.CharField(blank=False, max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(blank=False, auto_now=True)
    upt_user = models.CharField(blank=False, max_length=20, default='ADMIN')


class trPaymentModel(models.Model):
    date = models.DateField(blank=False, auto_now_add=True)
    receipt_no = models.IntegerField(blank=False, default=1)
    trHeader = models.ForeignKey('trHeaderModel', models.DO_NOTHING)
    seq = models.IntegerField(blank=False, default=1)
    cardComp = models.IntegerField(blank=False, default=0)
    cardNo = models.CharField(blank=False, max_length=16, default='0001000200030004')
    ins_dttm = models.DateTimeField(blank=False, auto_now_add=True)
    ins_user = models.CharField(blank=False, max_length=20, default='ADMIN')
    upt_dttm = models.DateTimeField(blank=False, auto_now=True)
    upt_user = models.CharField(blank=False, max_length=20, default='ADMIN')


#####tmp#####
class ItemModelTmp(models.Model):
    companyCode = models.CharField(blank=False, default='C0012', max_length=7)
    itemCode = models.CharField(blank=False, default='0001', max_length=7)
    barcode = models.CharField(blank=False, default='123213 2823', max_length=20)
    discountEndDttm = models.DateTimeField(blank=True, default='2020-03-28 23:00:00')
    discountPrice = models.FloatField()

class nabiImage(models.Model):
    photo = models.FileField(blank=False, null=False, upload_to="images")