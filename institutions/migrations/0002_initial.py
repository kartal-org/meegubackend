# Generated by Django 3.2.8 on 2021-11-30 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institutions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institutions_staff_related', related_query_name='institutions_staffs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='institutionverification',
            name='institution',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='institutions.institution'),
        ),
        migrations.AddField(
            model_name='department',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.institution'),
        ),
        migrations.AlterUniqueTogether(
            name='staff',
            unique_together={('user', 'institution')},
        ),
        migrations.AlterUniqueTogether(
            name='department',
            unique_together={('name', 'institution')},
        ),
    ]
