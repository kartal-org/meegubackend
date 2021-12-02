# Generated by Django 3.2.8 on 2021-12-02 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workspaces', '0004_workspace_leader'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workspace',
            old_name='leader',
            new_name='creator',
        ),
        migrations.RemoveField(
            model_name='workspace',
            name='members',
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')], default='approved', max_length=10)),
                ('role', models.CharField(choices=[('leader', 'Leader'), ('member', 'Member')], default='member', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workspaces_member_related', related_query_name='workspaces_members', to=settings.AUTH_USER_MODEL)),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspaces.workspace')),
            ],
            options={
                'unique_together': {('user', 'workspace')},
            },
        ),
    ]