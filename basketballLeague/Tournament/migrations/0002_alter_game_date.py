# Generated by Django 5.0.6 on 2024-05-20 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tournament', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
