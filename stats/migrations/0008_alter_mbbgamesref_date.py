# Generated by Django 4.2.7 on 2023-11-30 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0007_remove_mbbstatlinesref_field_goal_pct_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mbbgamesref',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
