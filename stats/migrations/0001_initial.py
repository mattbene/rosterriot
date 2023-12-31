# Generated by Django 4.2.7 on 2023-11-08 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mbb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MbbGameEspn',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='espn unique game id')),
                ('home_id', models.PositiveIntegerField(verbose_name='home team espn id')),
                ('home_points', models.PositiveSmallIntegerField(verbose_name='home team total points')),
                ('away_id', models.PositiveIntegerField(verbose_name='away team espn id')),
                ('away_points', models.PositiveSmallIntegerField(verbose_name='home team total points')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('location', models.CharField(max_length=64)),
                ('spread', models.DecimalField(decimal_places=1, max_digits=3)),
                ('total', models.DecimalField(decimal_places=1, max_digits=4, verbose_name='combined point total')),
                ('favorite', models.CharField(max_length=64, verbose_name='vegas favorite')),
                ('is_final', models.BooleanField()),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='espn_games', to='mbb.season')),
            ],
        ),
        migrations.CreateModel(
            name='MbbGameSref',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, verbose_name='sref unique game id')),
                ('date', models.DateTimeField()),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(max_length=64)),
                ('arena', models.CharField(max_length=64)),
                ('team_one_id', models.CharField(max_length=64, verbose_name='sref team one id')),
                ('score_one', models.PositiveSmallIntegerField()),
                ('team_two_id', models.CharField(max_length=64, verbose_name='sref team one id')),
                ('score_two', models.PositiveSmallIntegerField()),
                ('favorite', models.CharField(max_length=64, verbose_name='vegas favorite')),
                ('spread', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='vegas spread')),
                ('total', models.DecimalField(decimal_places=1, max_digits=4, verbose_name='combined point total')),
                ('result', models.CharField(max_length=5, verbose_name='over/under result')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sref_games', to='mbb.season')),
            ],
        ),
        migrations.CreateModel(
            name='MbbStatlineSref',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.CharField(max_length=64, verbose_name='sref player id')),
                ('minutes', models.SmallIntegerField(verbose_name='minutes played')),
                ('field_goals', models.SmallIntegerField()),
                ('field_goal_att', models.SmallIntegerField()),
                ('field_goal_pct', models.DecimalField(decimal_places=3, max_digits=4)),
                ('two_pts', models.SmallIntegerField()),
                ('two_pt_att', models.SmallIntegerField()),
                ('two_pt_pct', models.DecimalField(decimal_places=3, max_digits=4)),
                ('three_pts', models.SmallIntegerField()),
                ('three_pt_att', models.SmallIntegerField()),
                ('three_pt_pct', models.DecimalField(decimal_places=3, max_digits=4)),
                ('free_throws', models.SmallIntegerField()),
                ('free_throw_att', models.SmallIntegerField()),
                ('free_throw_pct', models.DecimalField(decimal_places=3, max_digits=4)),
                ('reb_o', models.SmallIntegerField()),
                ('reb_d', models.SmallIntegerField()),
                ('rebounds', models.SmallIntegerField()),
                ('assists', models.SmallIntegerField()),
                ('steals', models.SmallIntegerField()),
                ('blocks', models.SmallIntegerField()),
                ('turnovers', models.SmallIntegerField()),
                ('fouls', models.SmallIntegerField()),
                ('points', models.SmallIntegerField()),
                ('game_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sref_statlines', to='stats.mbbgamesref')),
            ],
        ),
        migrations.CreateModel(
            name='MbbStatlineEspn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.PositiveIntegerField(verbose_name='espn player id')),
                ('started_game', models.BooleanField()),
                ('field_goals', models.SmallIntegerField()),
                ('shot_attempts', models.SmallIntegerField()),
                ('three_pointers', models.SmallIntegerField()),
                ('three_pt_att', models.SmallIntegerField()),
                ('free_throw_makes', models.SmallIntegerField()),
                ('free_throw_att', models.SmallIntegerField()),
                ('points', models.SmallIntegerField()),
                ('rebounds', models.SmallIntegerField()),
                ('assists', models.SmallIntegerField()),
                ('steals', models.SmallIntegerField()),
                ('blocks', models.SmallIntegerField()),
                ('turnovers', models.SmallIntegerField()),
                ('fouls', models.SmallIntegerField()),
                ('game_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='espn_statlines', to='stats.mbbgameespn')),
            ],
        ),
    ]
