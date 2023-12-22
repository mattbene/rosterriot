from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from stats.models import MbbGameEspn, MbbGameSref

class Command(BaseCommand):
    help = "Builds a new set of games from the two game data source tables."

    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        #return super().handle(*args, **options)
        games_espn = MbbGameEspn.objects.all()
        games_sref = MbbGameSref.objects.all()

       #for espn in games_espn:






        '''for school in School.objects.all():
            school.name = school.name.strip()
            school.short_name = school.short_name.strip()
            school.mascot = school.mascot.strip()
            school.abbr = school.abbr.strip()
            school.save()'''
        return "Schools table values cleaned."