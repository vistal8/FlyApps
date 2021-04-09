# Generated by Django 3.0.3 on 2021-03-29 15:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0026_auto_20210329_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='actual_download_gift_times',
            field=models.BigIntegerField(default=0, verbose_name='实际赠送的数量'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='actual_download_times',
            field=models.BigIntegerField(default=0, verbose_name='实际购买的数量'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='actual_amount',
            field=models.BigIntegerField(verbose_name='实付金额,单位分'),
        ),
        migrations.AlterField(
            model_name='price',
            name='price',
            field=models.BigIntegerField(verbose_name='下载包价格，单位分'),
        ),
    ]