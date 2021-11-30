# Generated by Django 3.2.8 on 2021-11-30 07:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import files.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institutions', '0001_initial'),
        ('classrooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassroomResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('published', 'published'), ('draft', 'draft')], default='draft', max_length=10)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('cover', models.ImageField(blank=True, default='userProfile/coverDefault_pdrisr.jpg', null=True, upload_to=files.models.upload_cover_to, verbose_name='Cover')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classrooms.classroom')),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.institution')),
            ],
            options={
                'unique_together': {('classroom', 'name')},
            },
        ),
        migrations.CreateModel(
            name='InstitutionResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('published', 'published'), ('draft', 'draft')], default='draft', max_length=10)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('cover', models.ImageField(blank=True, default='userProfile/coverDefault_pdrisr.jpg', null=True, upload_to=files.models.upload_cover_to, verbose_name='Cover')),
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
            name='ClassroomResourceFolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.classroomresource')),
            ],
            options={
                'unique_together': {('name', 'resource')},
            },
        ),
        migrations.CreateModel(
            name='InstitutionResourceFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=10)),
                ('tags', models.CharField(blank=True, max_length=10, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('size', models.PositiveIntegerField(default=0)),
                ('file', models.FileField(blank=True, null=True, upload_to=files.models.upload_to)),
                ('content', models.TextField(blank=True, null=True)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources_institutionresourcefile_related', related_query_name='resources_institutionresourcefiles', to='resources.institutionresourcefolder')),
            ],
            options={
                'unique_together': {('name', 'folder')},
            },
        ),
        migrations.CreateModel(
            name='ClassroomResourceFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=10)),
                ('tags', models.CharField(blank=True, max_length=10, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('size', models.PositiveIntegerField(default=0)),
                ('file', models.FileField(blank=True, null=True, upload_to=files.models.upload_to)),
                ('content', models.TextField(blank=True, null=True)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources_classroomresourcefile_related', related_query_name='resources_classroomresourcefiles', to='resources.classroomresourcefolder')),
            ],
            options={
                'unique_together': {('name', 'folder')},
            },
        ),
    ]
