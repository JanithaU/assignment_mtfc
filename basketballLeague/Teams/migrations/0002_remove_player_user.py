# Generated by Django 5.0.6 on 2024-05-17 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Teams', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='user',
        ),
    ]