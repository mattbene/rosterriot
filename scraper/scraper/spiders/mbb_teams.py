import scrapy
from bs4 import BeautifulSoup

class MbbTeamsSpider(scrapy.Spider):
    name = "mbb_teams"
    allowed_domains = ["espn.com"]
    start_urls = ["https://www.espn.com/mens-college-basketball/teams"]

    def parse(self, response):
        for conference in response.css('div.mt7'):
            for school in conference.css('div.pl3'):
                yield {
                    'team': school.css('h2::text').get(),
                    'conference': conference.css('div.headline::text').get(),
                    'espn_id': int(school.css('a.AnchorLink::attr(href)').get().split('/')[-2]),
                }