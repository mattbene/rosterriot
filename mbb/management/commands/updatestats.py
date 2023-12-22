from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from mbb.models import Season, School, Team, Game, Statline
from stats.models import MbbStatlineEspn, MbbStatlineSref
from datetime import date

class Command(BaseCommand):
    help = "Updates the MBB Games Table from the ESPN Game AND Sports-Reference Game Tables"

    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        current_season = Season.objects.get(end_date=None).year
        #return super().handle(*args, **options)
        #espns = MbbGameEspn.objects.filter(season_id=current_season, date=date(2023,11,6))
        #srefs = MbbGameSref.objects.filter(season_id=current_season, date=date(2023,11,6))