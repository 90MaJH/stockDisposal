# Generated by Django 3.0.2 on 2020-03-10 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200310_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemmodeltmp',
            name='discountEndDttm',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='itemmodeltmp',
            name='discountPrice',
            field=models.FloatField(null=True),
        ),
    ]
