# Generated by Django 3.2.8 on 2021-12-01 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0005_alter_institution_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institution',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]