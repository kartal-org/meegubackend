# Generated by Django 3.2.8 on 2021-12-01 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroommember',
            name='status',
            field=models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')], default='approved', max_length=10),
        ),
    ]