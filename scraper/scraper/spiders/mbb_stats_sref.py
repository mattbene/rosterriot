from typing import Any, Optional
import scrapy


class MbbStatsSrefSpider(scrapy.Spider):
    name = "mbb_stats_sref"
    allowed_domains = ["sports-reference.com"]
    """custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.MbbStatsSrefPipeline': 400
        }
    }"""
    def __init__(self, month = None, day = None, year = None, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.month = month
        self.day = day
        self.year = year
        if month == None and day == None and year == None:
            self.start_urls = ["https://sports-reference.com/cbb/boxscores"]
        else:
            self.start_urls = [f"https://sports-reference.com/cbb/boxscores/index.cgi?month={month}&day={day}&year={year}"]

    def parse(self, response):
        for game in response.css('div.gender-m'):
            #yield {'href': game.css('td.gamelink').css('a').attrib['href']}
            yield scrapy.Request('https://sports-reference.com/' + game.css('td.gamelink').css('a').attrib['href'], callback=self.parse_game, cb_kwargs=dict(game_id=game.attrib['id']))
    
    def parse_game(self, response):
        content = response.css('#boxes')