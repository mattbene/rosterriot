from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from mbb.models import School, Team, Season, Game
from stats.models import MbbGameEspn, MbbGameSref
from datetime import date, timedelta

class Command(BaseCommand):
    help = "Updates the MBB Games Table from the ESPN Game AND Sports-Reference Game Tables"

    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        current_season = Season.objects.get(end_date=None).year
        #return super().handle(*args, **options)
        #espns = MbbGameEspn.objects.filter(season_id=current_season, date=date(2023,11,6))
        srefs = MbbGameSref.objects.filter(season_id=current_season).exclude(score_two=None)

        for sref in srefs:
            print(f"Working on game between {sref.team_one_id} and {sref.team_two_id}")
            try:
                try:
                    espn = MbbGameEspn.objects.get(date=sref.date, home_id=School.objects.get(sref_id=sref.team_two_id).espn_id, away_id=School.objects.get(sref_id=sref.team_one_id).espn_id)
                except:
                    new = sref.date + timedelta(days=-1)
                    #print(f"Trying date: {new}")
                    espn = MbbGameEspn.objects.get(date=new, home_id=School.objects.get(sref_id=sref.team_two_id).espn_id, away_id=School.objects.get(sref_id=sref.team_one_id).espn_id)
            except:
                try:
                    espn = MbbGameEspn.objects.get(date=sref.date, home_id=School.objects.get(sref_id=sref.team_one_id).espn_id, away_id=School.objects.get(sref_id=sref.team_two_id).espn_id)
                except:
                    new = sref.date + timedelta(days=-1)
                    #print(f"Trying date: {new}")
                    espn = MbbGameEspn.objects.get(date=new, home_id=School.objects.get(sref_id=sref.team_one_id).espn_id, away_id=School.objects.get(sref_id=sref.team_two_id).espn_id)
            
            home_team = Team.objects.get(season_id=current_season, school_id=School.objects.get(espn_id=espn.home_id)).id
            away_team = Team.objects.get(season_id=current_season, school_id=School.objects.get(espn_id=espn.away_id)).id
            
            Game.objects.update_or_create(
                date = espn.date,
                home_team_id = home_team,
                away_team_id = away_team,
                season_id = current_season,
                defaults = {
                    'time': espn.time,
                    'location': espn.location,
                    'arena': espn.arena,
                    'spread': espn.spread,
                    'total': espn.total,
                    'favorite': espn.favorite,
                    'is_final': True,
                    'home_points': sref.score_two,
                    'away_points': sref.score_one,
                    'espn_id': espn.id,
                    'sref_id': sref.id,
                }
            )
            #print(f"Game between {sref.team_one_id} and {sref.team_two_id} updated.")
        return "MBB Games Table Successfully Updated."