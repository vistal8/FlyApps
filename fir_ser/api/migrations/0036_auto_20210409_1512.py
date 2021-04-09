# Generated by Django 3.0.3 on 2021-04-09 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_usercertificationinfo_reviewed_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercertificationinfo',
            name='user_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='certification', to=settings.AUTH_USER_MODEL, verbose_name='用户ID'),
        ),
    ]