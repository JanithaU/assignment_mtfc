# Generated by Django 5.0.6 on 2024-05-17 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teams', '0002_remove_player_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='field_goals',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='games_played',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]