# Generated by Django 3.2.8 on 2021-11-21 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workspaces', '0003_isnotamember'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='workspace',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workspaces.workspace'),
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together={('user', 'workspace')},
        ),
        migrations.RemoveField(
            model_name='member',
            name='classroom',
        ),
    ]
