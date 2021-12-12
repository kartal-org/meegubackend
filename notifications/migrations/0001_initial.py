# Generated by Django 3.2.8 on 2021-12-12 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('verification', 'verification'), ('submission', 'submission'), ('recommendation', 'recommendation')], max_length=20)),
                ('message', models.TextField(blank=True, null=True)),
                ('isRead', models.BooleanField(default=False)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateModified', models.DateTimeField(auto_now=True)),
                ('redirectID', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-dateModified'],
            },
        ),
    ]
