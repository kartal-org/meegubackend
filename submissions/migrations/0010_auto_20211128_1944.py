# Generated by Django 3.2.8 on 2021-11-28 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0008_auto_20211128_1934'),
        ('submissions', '0009_remove_submission_workspace'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='uploadfile',
        ),
        migrations.AlterField(
            model_name='submission',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='submission_files', to='workspaces.workspacefile'),
        ),
    ]
