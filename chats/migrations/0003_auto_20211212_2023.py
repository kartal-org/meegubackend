# Generated by Django 3.2.8 on 2021-12-12 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicchatroom',
            name='users',
        ),
        migrations.RemoveField(
            model_name='publicroomchatmessage',
            name='room',
        ),
        migrations.RemoveField(
            model_name='publicroomchatmessage',
            name='user',
        ),
        migrations.DeleteModel(
            name='Conversation',
        ),
        migrations.DeleteModel(
            name='PublicChatRoom',
        ),
        migrations.DeleteModel(
            name='PublicRoomChatMessage',
        ),
    ]
