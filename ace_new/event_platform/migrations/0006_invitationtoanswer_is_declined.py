# Generated by Django 2.0.1 on 2018-02-05 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_platform', '0005_auto_20180205_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitationtoanswer',
            name='is_declined',
            field=models.BooleanField(default=False),
        ),
    ]
