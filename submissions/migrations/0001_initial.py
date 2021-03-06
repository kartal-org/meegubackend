# Generated by Django 3.2.8 on 2021-12-12 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecommendationResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateModified', models.DateTimeField(auto_now=True)),
                ('responseStatus', models.CharField(choices=[('accepted', 'Accepted'), ('revise', 'Revise'), ('rejected', 'Rejected'), ('pending', 'Pending'), ('published', 'Published')], max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateUpdated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('submit', 'Submit')], default='draft', max_length=10)),
            ],
            options={
                'ordering': ['-dateUpdated'],
            },
        ),
        migrations.CreateModel(
            name='SubmissionResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responseStatus', models.CharField(choices=[('accepted', 'Accepted'), ('revise', 'Revise'), ('rejected', 'Rejected'), ('pending', 'Pending')], default='pending', max_length=20)),
                ('comment', models.TextField(blank=True, null=True)),
                ('dateCreated', models.DateTimeField(auto_now_add=True)),
                ('dateModified', models.DateTimeField(auto_now=True)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submissions.submission')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
