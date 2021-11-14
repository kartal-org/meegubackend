# Generated by Django 3.2.8 on 2021-11-14 03:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=50)),
                ('content', models.TextField(blank=True, null=True)),
                ('dateCreated', models.DateTimeField(default=django.utils.timezone.now)),
                ('dateUpdated', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-dateUpdated',),
                'unique_together': {('owner', 'title')},
            },
        ),
    ]
