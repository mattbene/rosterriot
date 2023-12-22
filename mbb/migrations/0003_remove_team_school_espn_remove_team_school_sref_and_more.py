# Generated by Django 4.2.7 on 2023-11-10 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mbb', '0002_school_mascot_school_short_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='school_espn',
        ),
        migrations.RemoveField(
            model_name='team',
            name='school_sref',
        ),
        migrations.AddField(
            model_name='team',
            name='school',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mbb.school'),
            preserve_default=False,
        ),
    ]
