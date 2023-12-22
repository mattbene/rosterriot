from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from mbb.models import School, Team, Season

class Command(BaseCommand):
    help = "Builds new versions of teams for a new season with data from the schools table."

    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        #return super().handle(*args, **options)
        for school in School.objects.all().order_by("name"):
            Team.objects.update_or_create(
                school = school,
                season_id = Season.objects.get(end_date=None).year,
                defaults = {
                    'name': f"{school.short_name} {school.mascot}",
                }
            )
            #print(f"Updated: {school.name}")
        return "MBB Teams Table Successfully Updated."