# Generated by Django 2.0.1 on 2018-02-11 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_platform', '0013_user_interested_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(related_name='tagged_questions', to='event_platform.Tag'),
        ),
    ]
