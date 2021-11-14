# Generated by Django 3.2.8 on 2021-11-14 03:22

from django.db import migrations, models
import django.db.models.deletion
import resources.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classrooms', '0001_initial'),
        ('institutions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassroomResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('published', 'published'), ('draft', 'draft')], default='draft', max_length=10)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classrooms.classroom')),
                ('institution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.institution')),
            ],
            options={
                'ordering': ('-dateUpdated',),
                'abstract': False,
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
            name='ClassroomResourceUploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=10)),
                ('tags', models.CharField(blank=True, max_length=10, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to=resources.models.upload_to)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources_classroomresourceuploadedfile_related', related_query_name='resources_classroomresourceuploadedfiles', to='resources.classroomresourcefolder')),
            ],
            options={
                'unique_together': {('name', 'folder')},
            },
        ),
        migrations.CreateModel(
            name='ClassroomResourceQuillFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=10)),
                ('tags', models.CharField(blank=True, max_length=10, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources_classroomresourcequillfile_related', related_query_name='resources_classroomresourcequillfiles', to='resources.classroomresourcefolder')),
            ],
            options={
                'unique_together': {('name', 'folder')},
            },
        ),
    ]
