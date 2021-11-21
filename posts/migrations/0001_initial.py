# Generated by Django 3.2.8 on 2021-11-17 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institutions', '0008_alter_staff_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=250, unique=True)),
                ('file', models.FileField(upload_to=posts.models.upload_to)),
                ('abstract', models.TextField()),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('publishedDate', models.DateTimeField(auto_now_add=True)),
                ('dateModified', models.DateTimeField(auto_now=True)),
                ('privacy', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='public', max_length=10)),
                ('author', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('category', models.ManyToManyField(blank=True, null=True, to='posts.Category')),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.institution')),
            ],
        ),
    ]