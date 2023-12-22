from django.db import models
from mbb.models import Season

# Create your models here.

### MENS BASKETBALL ###

class MbbGameEspn(models.Model):
    id = models.PositiveIntegerField(primary_key=True, verbose_name='espn unique game id')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='espn_games')
    home_id = models.PositiveIntegerField(null=True, verbose_name='home team espn id')
    home_points = models.PositiveSmallIntegerField(null=True, verbose_name='home team total points')
    away_id = models.PositiveIntegerField(null=True, verbose_name='away team espn id')
    away_points = models.PositiveSmallIntegerField(null=True, verbose_name='home team total points')
    date = models.DateField()
    time = models.TimeField(null=True)
    location = models.CharField(max_length=64, null=True)
    arena = models.CharField(max_length=64, null=True)
    spread = models.DecimalField(decimal_places=1, max_digits=3, null=True)
    total = models.DecimalField(decimal_places=1, max_digits=4, null=True, verbose_name='combined point total')
    favorite = models.CharField(max_length=64, null=True, verbose_name='vegas favorite')
    is_final = models.BooleanField(default=False)

class MbbGameSref(models.Model):
    id = models.CharField(primary_key=True, max_length=64, verbose_name='sref unique game id')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='sref_games')
    date = models.DateField(null=True)
    city = models.CharField(max_length=64, null=True)
    state = models.CharField(max_length=64, null=True)
    arena = models.CharField(max_length=64, null=True)
    team_one_id = models.CharField(max_length=64, null=True, verbose_name='sref team one id')
    score_one = models.PositiveSmallIntegerField(null=True)
    team_two_id = models.CharField(max_length=64, null=True, verbose_name='sref team one id')
    score_two = models.PositiveSmallIntegerField(null=True)
    favorite = models.CharField(max_length=64, null=True, verbose_name='vegas favorite')
    spread = models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name='vegas spread')
    total = models.DecimalField(decimal_places=1, max_digits=4, null=True, verbose_name='combined point total')
    result = models.CharField(max_length=5, null=True, verbose_name='over/under result')

class MbbStatlineEspn(models.Model):
    game_code = models.ForeignKey(MbbGameEspn, on_delete=models.CASCADE, related_name='espn_statlines')
    player_id = models.PositiveIntegerField(verbose_name='espn player id')
    started_game = models.BooleanField()
    minutes = models.SmallIntegerField(null=True)
    field_goals = models.SmallIntegerField()
    shot_attempts = models.SmallIntegerField()
    three_pointers = models.SmallIntegerField()
    three_pt_att = models.SmallIntegerField()
    free_throw_makes = models.SmallIntegerField()
    free_throw_att = models.SmallIntegerField()
    points = models.SmallIntegerField()
    off_reb = models.SmallIntegerField(null=True)
    def_reb = models.SmallIntegerField(null=True)
    rebounds = models.SmallIntegerField()
    assists = models.SmallIntegerField()
    steals = models.SmallIntegerField()
    blocks = models.SmallIntegerField()
    turnovers = models.SmallIntegerField()
    fouls = models.SmallIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['game_code', 'player_id'])
        ]

class MbbStatlineSref(models.Model):
    game_code = models.ForeignKey(MbbGameSref, on_delete=models.CASCADE, related_name='sref_statlines')
    player_id = models.CharField(max_length=64, verbose_name='sref player id')
    minutes = models.SmallIntegerField(verbose_name='minutes played')
    field_goals = models.SmallIntegerField()
    field_goal_att = models.SmallIntegerField()
    #field_goal_pct = models.DecimalField(decimal_places=3, max_digits=4)
    two_pts = models.SmallIntegerField()
    two_pt_att = models.SmallIntegerField()
    #two_pt_pct = models.DecimalField(decimal_places=3, max_digits=4)
    three_pts = models.SmallIntegerField()
    three_pt_att = models.SmallIntegerField()
    #three_pt_pct = models.DecimalField(decimal_places=3, max_digits=4)
    free_throws = models.SmallIntegerField()
    free_throw_att = models.SmallIntegerField()
    #free_throw_pct = models.DecimalField(decimal_places=3, max_digits=4)
    reb_o = models.SmallIntegerField()
    reb_d = models.SmallIntegerField()
    rebounds = models.SmallIntegerField()
    assists = models.SmallIntegerField()
    steals = models.SmallIntegerField()
    blocks = models.SmallIntegerField()
    turnovers = models.SmallIntegerField()
    fouls = models.SmallIntegerField()
    points = models.SmallIntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['game_code', 'player_id'])
        ]