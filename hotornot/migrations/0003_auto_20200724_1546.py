# Generated by Django 3.0.8 on 2020-07-24 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotornot', '0002_auto_20200724_1545'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hot_post',
            old_name='hottimage',
            new_name='hotimage',
        ),
    ]