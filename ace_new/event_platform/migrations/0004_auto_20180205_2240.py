# Generated by Django 2.0.1 on 2018-02-05 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_platform', '0003_answerinvitation'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AnswerInvitation',
            new_name='InvitationToAnswer',
        ),
    ]
