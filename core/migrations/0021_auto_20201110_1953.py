# Generated by Django 2.2.8 on 2020-11-10 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20201110_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sendmessage',
            name='members',
        ),
        migrations.RemoveField(
            model_name='sendmessage',
            name='send_to_members',
        ),
        migrations.AddField(
            model_name='profile',
            name='message',
            field=models.TextField(default='Hello........'),
        ),
        migrations.AddField(
            model_name='profile',
            name='send_message',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='subject',
            field=models.CharField(default='StudentsEarn...', max_length=200),
        ),
    ]
