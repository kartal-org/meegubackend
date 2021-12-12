# Generated by Django 3.2.8 on 2021-12-12 02:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('libraries', '0002_libraryitem_publication'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryitem',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='libraryitem',
            unique_together={('user', 'publication')},
        ),
    ]
