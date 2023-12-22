import scrapy


class MbbSchoolsEspnSpider(scrapy.Spider):
    name = "mbb_schools_espn"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.MbbSchoolsEspnPipeline': 300
        }
    }
    allowed_domains = ["espn.com", "duckduckgo.com"]
    start_urls = [
        "https://www.espn.com/mens-college-basketball/teams",
        

                  ]

    def parse(self, response):
        # Link One Below
        """for conference in response.css('div.mt7'):
            for school in conference.css('div.pl3'):
                yield {
                    'team': school.css('h2::text').get(),
                    'conference': conference.css('div.headline::text').get(),
                    'espn_id': int(school.css('a.AnchorLink::attr(href)').get().split('/')[-2]),
                }"""
