# Generated by Django 3.2.8 on 2021-12-13 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0002_auto_20211213_1808'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='workspacefile',
            unique_together=set(),
        ),
    ]
