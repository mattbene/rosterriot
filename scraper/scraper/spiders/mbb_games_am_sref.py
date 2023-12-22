import scrapy
from datetime import datetime, date

class MbbGamesAmSrefSpider(scrapy.Spider):
    name = "mbb_games_am_sref"
    allowed_domains = ["sports-reference.com"]
    start_urls = [f"https://sports-reference.com/cbb/boxscores/index.cgi?{datetime.strftime(date.today(),'month=%m&day=%d&year=%Y')}"]

    def parse(self, response):
        for game in response.css('div.gender-m'):
            yield {
                
            }