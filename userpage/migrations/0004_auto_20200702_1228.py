# Generated by Django 3.0.6 on 2020-07-02 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0003_auto_20200702_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(upload_to='media/%Y/%m/%d'),
        ),
    ]
