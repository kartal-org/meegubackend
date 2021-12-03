# Generated by Django 3.2.8 on 2021-12-03 01:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0004_chatroom_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='is_readBy',
            field=models.ManyToManyField(blank=True, help_text='Members who read the chat.', related_name='read_by', to=settings.AUTH_USER_MODEL),
        ),
    ]