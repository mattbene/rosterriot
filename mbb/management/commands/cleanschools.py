from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from mbb.models import School
import scrapy
from scrapy.crawler import CrawlerProcess

class Command(BaseCommand):
    help = "Builds new versions of teams for a new season with data from the schools table."

    def add_arguments(self, parser: CommandParser) -> None:
        return super().add_arguments(parser)
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        #return super().handle(*args, **options)
        schools = School.objects.all()
        
        for school in schools:
            school.name = school.name.strip()
            school.city = school.city.strip()
            school.state = school.state.strip()
            school.short_name = school.short_name.strip()
            school.mascot = school.mascot.strip()
            try:
                school.abbr = school.abbr.strip()
            except AttributeError:
                school.abbr = None
            school.save()
        return "Schools table values stripped."