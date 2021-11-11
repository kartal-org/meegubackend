# Generated by Django 3.2.8 on 2021-11-11 15:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import workspaces.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=8, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=10)),
                ('dateCreated', models.DateTimeField(default=django.utils.timezone.now)),
                ('dateUpdated', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-dateUpdated',),
            },
        ),
        migrations.CreateModel(
            name='WorkspaceFolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('workspace', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workspace_folder', to='workspaces.workspace')),
            ],
            options={
                'unique_together': {('name', 'workspace')},
            },
        ),
        migrations.CreateModel(
            name='WorkspaceUploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=10)),
                ('tags', models.CharField(blank=True, max_length=10, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to=workspaces.models.upload_to)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workspaces_workspaceuploadedfile_related', related_query_name='workspaces_workspaceuploadedfiles', to=settings.AUTH_USER_MODEL)),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workspaces_workspaceuploadedfile_related', related_query_name='workspaces_workspaceuploadedfiles', to='workspaces.workspacefolder')),
            ],
            options={
                'unique_together': {('name', 'folder')},
            },
        ),
        migrations.CreateModel(
            name='WorkspaceQuillFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=10)),
                ('tags', models.CharField(blank=True, max_length=10, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workspaces_workspacequillfile_related', related_query_name='workspaces_workspacequillfiles', to=settings.AUTH_USER_MODEL)),
                ('folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workspaces_workspacequillfile_related', related_query_name='workspaces_workspacequillfiles', to='workspaces.workspacefolder')),
            ],
            options={
                'unique_together': {('name', 'folder')},
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('accepted', 'accepted'), ('rejected', 'rejected'), ('pending', 'pending')], default='accepted', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members_workspace', to='workspaces.workspace')),
            ],
            options={
                'unique_together': {('user', 'workspace')},
            },
        ),
    ]
