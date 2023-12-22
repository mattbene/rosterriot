import scrapy


class MbbGamestatsEspnSpider(scrapy.Spider):
    name = "mbb_gamestats_espn"
    """custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.MbbGameStatsEspnPipeline': 300
        }
    }"""
    allowed_domains = ["espn.com"]
    start_urls = ["https://www.espn.com/mens-college-basketball/scoreboard/_/seasontype/2/group/50"]

    def parse(self, response):
        card = response.css('section.gameModules')
        header = card.css('header::attr(aria-label)').get()
        for game in card.css('section'):

            '''yield {
                'id': game.css('::attr(id)').get(),
                'away_id':,
                'away_pts':,
                'home_id':,
                'home_pts':,
                'date':,
                'time':,
                'location':,
                'spread':,
                'favorite':,
                'is_final': game.css('div.ScoreCell__Time::text').get(),
            }'''