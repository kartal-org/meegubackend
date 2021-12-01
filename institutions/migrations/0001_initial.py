# Generated by Django 3.2.8 on 2021-12-01 04:08

from django.db import migrations, models
import django.db.models.deletion
import institutions.models
import members.models
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(default='userProfile/default_egry2i.jpg', upload_to=institutions.models.upload_to_department, verbose_name='Profile')),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateModified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-dateModified',),
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('privacy', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='private', max_length=10)),
                ('cover', models.ImageField(default='userProfile/coverDefault_pdrisr.jpg', upload_to=products.models.upload_to, verbose_name='Cover')),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('image', models.ImageField(default='userProfile/default_egry2i.jpg', upload_to=institutions.models.upload_to, verbose_name='Profile')),
                ('address', models.TextField()),
                ('contact', models.CharField(max_length=11, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('website', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ('-dateUpdated',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InstitutionVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('disapproved', 'Disapproved')], default='pending', max_length=20)),
                ('document', models.FileField(blank=True, null=True, upload_to=institutions.models.upload_verification)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateModified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-dateModified',),
            },
        ),
        migrations.CreateModel(
            name='StaffType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('permissions', models.JSONField(default=members.models.defaultPermission)),
                ('custom_Type_For', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.institution')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('approved', 'Approved'), ('pending', 'Pending'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institutions.department')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.institution')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institutions.stafftype')),
            ],
        ),
    ]
