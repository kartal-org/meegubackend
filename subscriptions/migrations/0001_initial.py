# Generated by Django 3.2.8 on 2021-11-30 07:11

from django.db import migrations, models
import django.db.models.deletion
import subscriptions.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institutions', '0001_initial'),
        ('classrooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=10)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('limitations', models.JSONField(blank=True, default=subscriptions.models.Plan.storageSizeDefault, null=True)),
                ('type', models.CharField(choices=[('classroom', 'Classroom'), ('institution', 'Institution')], max_length=20)),
                ('cover', models.ImageField(default='userProfile/coverDefault_pdrisr.jpg', upload_to=subscriptions.models.upload_to, verbose_name='Cover')),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateModified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('name', 'type')},
            },
        ),
        migrations.CreateModel(
            name='InstitutionSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payer_Email', models.EmailField(max_length=254)),
                ('payer_FullName', models.CharField(max_length=255)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.institution')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.plan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClassroomSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payer_Email', models.EmailField(max_length=254)),
                ('payer_FullName', models.CharField(max_length=255)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classrooms.classroom')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscriptions.plan')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
