# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from mbb.models import School, Player, PlayerSeason
from stats.models import MbbGameEspn, MbbGameSref, MbbStatlineEspn, MbbStatlineSref

class SchoolItem(DjangoItem):
    django_model = School


class PlayerItem(DjangoItem):
    django_model = Player

class PlayerSeasonItem(DjangoItem):
    django_model = PlayerSeason

class MbbGameEspnItem(DjangoItem):
    django_model = MbbGameEspn

class MbbGameSrefItem(DjangoItem):
    django_model = MbbGameSref

class MbbStatlineEspnItem(DjangoItem):
    django_model = MbbStatlineEspn

class MbbStatlineSrefItem(DjangoItem):
    django_model = MbbStatlineSref

class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
