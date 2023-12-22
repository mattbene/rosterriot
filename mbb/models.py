from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Season(models.Model):
    year = models.PositiveIntegerField(primary_key=True)
    start_date = models.DateField(null=True, verbose_name='season start date')
    end_date = models.DateField(null=True, verbose_name='season end date')

    def __str__(self):
        return f'{int(self.year) - 1} - {self.year} Season'

class Conference(models.Model):
    name = models.CharField(max_length=64, null=True, verbose_name='conference long name')
    short = models.CharField(max_length=24, null=True, verbose_name='conference short name')
    abbr = models.CharField(max_length=6, null=True, verbose_name='conference abbreviation')
    first = models.PositiveSmallIntegerField(null=True, verbose_name='first conference season')
    last = models.PositiveSmallIntegerField(null=True, verbose_name='final conference season')
    
    def __str__(self):
        return self.name

class School(models.Model):
    name = models.CharField(max_length=64)
    short_name = models.CharField(max_length=64, null=True)
    mascot = models.CharField(max_length=64, null=True)
    city = models.CharField(max_length=64, null=True)
    state = models.CharField(max_length=64, null=True)
    logo = models.URLField(null=True, verbose_name='school logo')
    alt = models.URLField(null=True, verbose_name='alternative school image')
    abbr = models.CharField(max_length=6, null=True, verbose_name='school abbreviation')
    
    # Source-specific IDs
    espn_id = models.PositiveIntegerField(null=True, blank=True)
    sref_id = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=64)
    coach = models.CharField(max_length=64, null=True)
    
    # Foreign Key Relationships
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=64)
    hometown = models.CharField(max_length=64, null=True)
    high_school = models.CharField(max_length=128, null=True)
    top_100 = models.CharField(max_length=24, null=True)
    
    # Source-specific IDs
    espn_id = models.PositiveIntegerField(null=True, blank=True)
    sref_id = models.CharField(max_length=64, null=True, blank=True)

    # Many-to-many Relationship with Season
    seasons = models.ManyToManyField(Season, through='PlayerSeason', related_name='players')

    def __str__(self):
        return self.name

class Game(models.Model):
    date = models.DateField()
    time = models.TimeField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='games')
    home_points = models.PositiveSmallIntegerField(verbose_name='home team total points')
    away_points = models.PositiveSmallIntegerField(verbose_name='away team total points')
    location = models.CharField(max_length=64, null=True)
    arena = models.CharField(max_length=64, null=True)
    spread = models.DecimalField(decimal_places=1, max_digits=3, null=True, verbose_name='vegas point spread')
    total = models.DecimalField(decimal_places=1, max_digits=4, null=True, verbose_name='vegas combined point total')
    favorite = models.CharField(max_length=64, null=True, verbose_name='vegas favorite')
    is_final = models.BooleanField(default=False)
    espn_id = models.PositiveIntegerField(verbose_name='espn unique game id')
    sref_id = models.CharField(max_length=64, verbose_name='sref unique game id')

    # Foreign Key Relationships
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')

    class Meta:
        indexes = [
            models.Index(fields=['date', 'home_team', 'away_team'])
        ]

    def __str__(self):
        return f'Game on {self.date} between {self.home_team} (home) and {self.away_team} (away)'


class PlayerSeason(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    
    # Additional fields for that season
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(null=True, verbose_name='player number')
    position = models.CharField(max_length=2, null=True)
    height = models.DecimalField(decimal_places=4, max_digits=5, null=True)
    weight = models.PositiveSmallIntegerField(null=True)
    academic_year = models.CharField(max_length=2, null=True, verbose_name='player academic year')

class Statline(models.Model):
    # Common fields for statistics
    points = models.IntegerField()
    rebounds = models.IntegerField()
    assists = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()
    fouls = models.IntegerField()
    
    # Foreign Key Relationships
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player_season = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE)

class PostseasonTournament(models.Model):
    name = models.CharField(max_length=64)
    start_date = models.DateField(null=True, verbose_name='tournament start date')
    end_date = models.DateField(null=True, verbose_name='tournament end date')
    
    # Foreign Key Relationships
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PostseasonTeam(models.Model):
    # Foreign Key Relationships
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    tournament = models.ForeignKey(PostseasonTournament, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.team} in {self.tournament}"

class UserProfile(models.Model):
    ACCOUNT_STATUS_CHOICES = (
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('banned', 'Banned'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField()
    tag_line = models.CharField(max_length=128, null=True)
    legacy_status = models.BooleanField(default=False)
    premium_status = models.BooleanField(default=False)
    join_date = models.DateField()
    last_login = models.DateTimeField(null=True)
    account_status = models.CharField(max_length=10, choices=ACCOUNT_STATUS_CHOICES, default='active')
    league_wins = models.IntegerField(null=True, default=0)
    
class ScoringRule(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    # Define fields to represent scoring rules.
    points = models.PositiveSmallIntegerField(default=1)
    rebounds = models.PositiveSmallIntegerField(default=1)
    assists = models.PositiveSmallIntegerField(default=1)
    steals = models.PositiveSmallIntegerField(default=1)
    blocks = models.PositiveSmallIntegerField(default=1)
    turnovers = models.SmallIntegerField(default=-1)
    multiplier = models.PositiveSmallIntegerField(default=2)
    multiplier_seed = models.PositiveSmallIntegerField(default=12)
    
    def __str__(self):
        return self.name

class DraftRule(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    # Define fields for draft rules.
    snake_draft = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class RosterRule(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    # Define fields for roster settings.
    no_of_players = models.PositiveSmallIntegerField()
    
    def __str__(self):
        return self.name

class TradeRule(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    # Define fields for trade rules.
    enable = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class FantasyLeague(models.Model):
    name = models.CharField(max_length=64)
    commissioner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    founding_date = models.DateField(null=True, verbose_name='league foundation date')
    description = models.TextField(null=True)
    
    # Many-to-many Relatioinships
    participants = models.ManyToManyField(UserProfile, through='FantasyTeam', related_name='leagues')

    # One-to-one Relationships with rule models
    scoring_rules = models.OneToOneField(ScoringRule, on_delete=models.SET_NULL, null=True)
    draft_rules = models.OneToOneField(DraftRule, on_delete=models.SET_NULL, null=True)
    roster_settings = models.OneToOneField(RosterRule, on_delete=models.SET_NULL, null=True)
    trade_rules = models.OneToOneField(TradeRule, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class FantasyTeam(models.Model):
    name = models.CharField(max_length=64)
    
    # Foreign Key Relationships
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    league = models.ForeignKey(FantasyLeague, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class DraftedPlayer(models.Model):
    round_number = models.PositiveSmallIntegerField()

    # Foreign Key Relationships
    player_season = models.ForeignKey(PlayerSeason, on_delete=models.CASCADE)
    fantasy_team = models.ForeignKey(FantasyTeam, on_delete=models.CASCADE)

class FantasyTeamPlayer(models.Model):
    # Foreign Key Relationships
    fantasy_team = models.ForeignKey(FantasyTeam, on_delete=models.CASCADE)
    drafted_player = models.ForeignKey(DraftedPlayer, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.drafted_player} in {self.fantasy_team}"

class FantasyTeamScore(models.Model):
    total_score = models.DecimalField(decimal_places=2, max_digits=10)
    
    # Foreign Key Relationships
    team = models.ForeignKey(FantasyTeam, on_delete=models.CASCADE)
    tournament = models.ForeignKey(PostseasonTournament, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Score for {self.team} in {self.tournament}"