# Generated by Django 3.0.8 on 2020-08-10 13:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotornot', '0011_auto_20200731_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='hot_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
