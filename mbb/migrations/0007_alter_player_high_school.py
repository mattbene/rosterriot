# Generated by Django 4.2.7 on 2023-11-28 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mbb', '0006_alter_userprofile_league_wins_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='high_school',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
