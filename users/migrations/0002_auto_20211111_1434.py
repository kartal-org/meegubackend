# Generated by Django 3.2.8 on 2021-11-11 06:34

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='cover',
            field=models.ImageField(blank=True, default='userProfile/coverDefault_pdrisr.jpg', null=True, upload_to=users.models.upload_to, verbose_name='Cover'),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='image',
            field=models.ImageField(blank=True, default='userProfile/default_egry2i.jpg', null=True, upload_to=users.models.upload_to, verbose_name='Profile'),
        ),
    ]
