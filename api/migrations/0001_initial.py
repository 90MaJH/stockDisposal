# Generated by Django 3.0.2 on 2020-03-10 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemModelTmp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companyCode', models.CharField(default='C0012', max_length=7)),
                ('itemCode', models.CharField(default='0001', max_length=7)),
                ('barcode', models.CharField(default='123213 2823', max_length=20)),
                ('discountEndDttm', models.DateTimeField(blank=True, default='2020-03-28 23:00:00')),
                ('discountPrice', models.FloatField()),
            ],
        ),
    ]