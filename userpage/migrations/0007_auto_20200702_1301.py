# Generated by Django 3.0.6 on 2020-07-02 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0006_auto_20200702_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='postimage',
            field=models.ImageField(upload_to='media/%Y/%m/%d'),
        ),
    ]
