# Generated by Django 3.2.8 on 2021-11-30 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='posts.Category'),
        ),
    ]
