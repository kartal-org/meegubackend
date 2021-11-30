# Generated by Django 3.2.8 on 2021-11-30 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('resources', '0001_initial'),
        ('institutions', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classrooms', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutionresourcefile',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='institutionresourcefile',
            name='folder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources_institutionresourcefile_related', related_query_name='resources_institutionresourcefiles', to='resources.institutionresourcefolder'),
        ),
        migrations.AddField(
            model_name='institutionresource',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.department'),
        ),
        migrations.AddField(
            model_name='institutionresource',
            name='institution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.institution'),
        ),
        migrations.AddField(
            model_name='classroomresourcefolder',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resources.classroomresource'),
        ),
        migrations.AddField(
            model_name='classroomresourcefile',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='classroomresourcefile',
            name='folder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resources_classroomresourcefile_related', related_query_name='resources_classroomresourcefiles', to='resources.classroomresourcefolder'),
        ),
        migrations.AddField(
            model_name='classroomresource',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classrooms.classroom'),
        ),
        migrations.AddField(
            model_name='classroomresource',
            name='institution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.institution'),
        ),
        migrations.AlterUniqueTogether(
            name='institutionresourcefolder',
            unique_together={('name', 'resource')},
        ),
        migrations.AlterUniqueTogether(
            name='institutionresourcefile',
            unique_together={('name', 'folder')},
        ),
        migrations.AlterUniqueTogether(
            name='institutionresource',
            unique_together={('name', 'institution')},
        ),
        migrations.AlterUniqueTogether(
            name='classroomresourcefolder',
            unique_together={('name', 'resource')},
        ),
        migrations.AlterUniqueTogether(
            name='classroomresourcefile',
            unique_together={('name', 'folder')},
        ),
        migrations.AlterUniqueTogether(
            name='classroomresource',
            unique_together={('classroom', 'name')},
        ),
    ]
