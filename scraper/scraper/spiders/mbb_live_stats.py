from typing import Any, Iterable, Optional
import scrapy
import datetime

class MbbLiveStatsSpider(scrapy.Spider):
    name = "mbb_live_stats"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.MbbLiveStatsPipeline': 400
        }
    }
    allowed_domains = ["espn.com"]
    def __init__(self, month = None, day = None, year = None, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.month = month
        self.day = day
        self.year = year
        if year != None or month != None or day != None:
            self.start_urls = [f"https://www.espn.com/mens-college-basketball/scoreboard/_/date/{year}{month}{day}/seasontype/2/group/50"]
        else:
            self.start_urls = ['https://www.espn.com/mens-college-basketball/scoreboard/_/seasontype/2/group/50']
    
    def parse(self, response):
        for game in response.css('section.Scoreboard'): # THIS IS WHERE THE SCRIPT IS LIMITED
            for callout in game.css('div.Scoreboard__Callouts'):
                for link in callout.css('a'):
                    if link.css('::text').get() == 'Box Score':
                        boxscore = link.css('::attr(href)').get()
                        yield scrapy.Request('https://www.espn.com' + boxscore, self.parse_espn_boxscore, cb_kwargs=dict(game_id=game.attrib['id']))

    def parse_espn_boxscore(self, response, game_id):
        box = response.css('div.Boxscore')
        for table in box.css('div.ResponsiveTable'):
            statlines = {}
            names = table.css('tbody')[0]
            stats = table.css('tbody')[1]
            for name in names.css('tr'):
                index = int(name.attrib['data-idx'])
                try:
                    name.css('a::attr(href)').get().split('/')[-2].strip()
                    statlines[index] = {}
                    statlines[index]['player'] = int(name.css('a::attr(href)').get().split('/')[-2].strip())
                    statlines[index]['game_id'] = int(game_id)
                    if index < 6:
                        statlines[index]['start'] = True
                    else:
                        statlines[index]['start'] = False
                except:
                    continue
            for line in stats.css('tr'):
                index = int(line.attrib['data-idx'])
                try:
                    statlines[index]['field_goals'] = int(line.css('td')[-12].css('::text').get().split('-')[0].strip())
                    statlines[index]['shot_attempts'] = int(line.css('td')[-12].css('::text').get().split('-')[1].strip())
                    statlines[index]['three_pointers'] = int(line.css('td')[-11].css('::text').get().split('-')[0].strip())
                    statlines[index]['three_pt_att'] = int(line.css('td')[-11].css('::text').get().split('-')[1].strip())
                    statlines[index]['free_throw_makes'] = int(line.css('td')[-10].css('::text').get().split('-')[0].strip())
                    statlines[index]['free_throw_att'] = int(line.css('td')[-10].css('::text').get().split('-')[1].strip())
                    statlines[index]['oreb'] = int(line.css('td')[-9].css('::text').get().strip())
                    statlines[index]['dreb'] = int(line.css('td')[-8].css('::text').get().strip())
                    statlines[index]['rebounds'] = int(line.css('td')[-7].css('::text').get().strip())
                    statlines[index]['assists'] = int(line.css('td')[-6].css('::text').get().strip())
                    statlines[index]['steals'] = int(line.css('td')[-5].css('::text').get().strip())
                    statlines[index]['blocks'] = int(line.css('td')[-4].css('::text').get().strip())
                    statlines[index]['turnovers'] = int(line.css('td')[-3].css('::text').get().strip())
                    statlines[index]['fouls'] = int(line.css('td')[-2].css('::text').get().strip())
                    statlines[index]['points'] = int(line.css('td')[-1].css('::text').get().strip())
                    if len(line.css('td')) < 13:
                        statlines[index]['minutes'] = None
                    else:
                        try:
                            statlines[index]['minutes'] = int(line.css('td')[-13].css('::text').get().strip())
                        except ValueError:
                             statlines[index]['minutes'] = int(0)
                except (KeyError, ValueError):
                    continue
            yield statlines