# Generated by Django 3.2.8 on 2021-12-05 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0005_chatmessage_is_readby'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatroom',
            options={'ordering': ('-dateModified',)},
        ),
    ]
