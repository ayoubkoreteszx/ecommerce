# Generated by Django 3.1 on 2020-09-08 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20200907_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
