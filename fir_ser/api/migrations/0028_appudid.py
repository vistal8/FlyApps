# Generated by Django 3.0.3 on 2020-04-16 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_apps_issupersign'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUDID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('udid', models.CharField(db_index=True, max_length=64, unique=True, verbose_name='udid唯一标识')),
                ('product', models.CharField(db_index=True, max_length=64, verbose_name='产品')),
                ('serial', models.CharField(db_index=True, max_length=64, verbose_name='序列号')),
                ('version', models.CharField(db_index=True, max_length=64, verbose_name='型号')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('app_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Apps', verbose_name='属于哪个APP')),
            ],
            options={
                'verbose_name': '应用详情',
                'verbose_name_plural': '应用详情',
                'unique_together': {('app_id', 'udid')},
            },
        ),
    ]