from typing import Iterable
import scrapy
from scrapy.http import Request
from mbb.models import School
#from items import SchoolItem
from asgiref.sync import sync_to_async


class MbbPlayersSpider(scrapy.Spider):
    name = "mbb_players"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.MbbPlayersPipeline': 400
        }
    }
    allowed_domains = ["espn.com"]
    start_urls = ["https://www.espn.com/mens-college-basketball/teams"]
    
    def parse(self, response):
        for team in response.css('div.pl3'):
            code = team.css('a::attr(href)').get().split('/')[-2].strip()
            yield scrapy.Request(f"https://www.espn.com/mens-college-basketball/team/roster/_/id/{code}", )

    def parse_roster(self, response):
        table = response.css('tbody.Table__TBODY')
        for row in table.css('tr'):
            try:
                number = row.css('td')[1].css('span::text').get().strip()
            except:
                number = None
            yield {
                'school_espn': response.meta['team_id'],
                'name': row.css('td')[1].css('a::text').get().strip(),
                'espn_id': row.css('td')[1].css('a::attr(href)').get().split('/')[-2].strip(),
                'number': number,
                'position': row.css('td')[2].css('div::text').get().strip(),
                'height': row.css('td')[3].css('div::text').get().strip(),
                'weight': row.css('td')[4].css('div::text').get().strip(),
                'class': row.css('td')[5].css('div::text').get().strip(),
                'birthplace': row.css('td')[6].css('div::text').get().strip(),
                }