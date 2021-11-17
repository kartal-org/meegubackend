# Generated by Django 3.2.8 on 2021-11-15 10:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import files.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institutions', '0006_auto_20211115_1303'),
        ('resources', '0002_auto_20211114_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstitutionResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('published', 'published'), ('draft', 'draft')], default='draft', max_length=10)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.department')),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.institution')),
            ],
            options={
                'unique_together': {('name', 'institution')},
            },
        ),
        migrations.CreateModel(
            name='InstitutionResourceFolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.institutionresource')),
            ],
            options={
                'unique_together': {('name', 'resource')},
            },
        ),
        migrations.CreateModel(
            name='InstitutionResourceUploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=10)),
                ('tags', models.CharField(blank=True, max_length=10, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('size', models.PositiveIntegerField(default=0)),
                ('file', models.FileField(upload_to=files.models.upload_to)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources_institutionresourceuploadedfile_related', related_query_name='resources_institutionresourceuploadedfiles', to='resources.institutionresourcefolder')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InstitutionResourceQuillFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=10)),
                ('tags', models.CharField(blank=True, max_length=10, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources_institutionresourcequillfile_related', related_query_name='resources_institutionresourcequillfiles', to='resources.institutionresourcefolder')),
            ],
            options={
                'unique_together': {('name', 'folder')},
            },
        ),
    ]
