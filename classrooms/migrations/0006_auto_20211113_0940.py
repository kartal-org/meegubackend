# Generated by Django 3.2.8 on 2021-11-13 01:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('classrooms', '0005_classroomresourcefolder_institution'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('published', 'published'), ('draft', 'draft')], default='draft', max_length=10)),
                ('dateCreated', models.DateTimeField(default=django.utils.timezone.now)),
                ('dateUpdated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ('-dateUpdated',),
            },
        ),
        migrations.RemoveField(
            model_name='classroomresource',
            name='classroom',
        ),
        migrations.RenameField(
            model_name='classroom',
            old_name='adviser',
            new_name='owner',
        ),
        migrations.DeleteModel(
            name='ClassroomAllowedWorkspace',
        ),
        migrations.AddField(
            model_name='resource',
            name='classroom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='classrooms.classroom'),
        ),
        migrations.AlterField(
            model_name='classroomresourcefolder',
            name='resource',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='source_resource_folder', to='classrooms.resource'),
        ),
        migrations.DeleteModel(
            name='ClassroomResource',
        ),
    ]
