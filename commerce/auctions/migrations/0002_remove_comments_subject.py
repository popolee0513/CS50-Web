# Generated by Django 3.2.5 on 2021-07-10 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='subject',
        ),
    ]
