# Generated by Django 2.2.8 on 2020-10-25 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20201021_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rank',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='JEE Rank'),
        ),
    ]
