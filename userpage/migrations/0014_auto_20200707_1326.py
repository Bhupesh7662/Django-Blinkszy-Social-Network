# Generated by Django 3.0.6 on 2020-07-07 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0013_auto_20200707_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='userImage',
            field=models.ImageField(default='media/user.png', upload_to="media/profiles/%Y/%m/%d'"),
        ),
    ]