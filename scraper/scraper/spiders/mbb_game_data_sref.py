from typing import Any, Optional
import scrapy
from datetime import date, datetime
from bs4 import BeautifulSoup as BS


class MbbGameDataSrefSpider(scrapy.Spider):
    name = "mbb_game_data_sref"
    allowed_domains = ["sports-reference.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.MbbGameDataSrefPipeline': 400
        }
    }
    def __init__(self, month = None, day = None, year = None, name: str | None = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.month = month
        self.day = day
        self.year = year
        if month == None and day == None and year == None:
            self.start_urls = ["https://www.sports-reference.com/cbb/boxscores"]
        else:
            self.start_urls = [f"https://www.sports-reference.com/cbb/boxscores/index.cgi?month={month}&day={day}&year={year}"]

    def parse(self, response):
        for game in response.css('div.gender-m'): # SCRIPT LIMITER
            try:
                yield scrapy.Request('https://www.sports-reference.com' + game.css('td.gamelink').css('a').attrib['href'], callback=self.parse_game, meta=dict(game_id=game.css('td.gamelink').css('a').attrib['href'].rsplit('/', 1)[-1].split('.')[0]))
            except KeyError:
                continue

    def parse_game(self, response):
        scorebox = response.css('div.scorebox')
        game_meta = scorebox.css('div.scorebox_meta')
        boxes = []
        try:
            team_one = scorebox.css('strong').css('a::attr(href)')[0].get().split('/')[-3]
            boxes.append(response.css(f"#box-score-basic-{team_one}"))
            team_two = scorebox.css('strong').css('a::attr(href)')[1].get().split('/')[-3]
            boxes.append(response.css(f"#box-score-basic-{team_two}"))
        except IndexError:
            ids = []
            for table in response.css('#boxes').css('table'):
                if str(table.attrib['id']).startswith('box-score-basic-'):
                    boxes.append(table)
                    ids.append(table.attrib['id'].split('-', 3)[-1])
            team_one = ids[0]
            team_two = ids[1]
        
        scores = scorebox.css('div.score::text').getall()
    
        game_data = {
            'game_id': response.meta['game_id'],
            'team_one': team_one,
            'score_one': int(scores[0].strip()),
            'team_two': team_two,
            'score_two': int(scores[1].strip()),
            'date': datetime.strptime(response.css('h1::text').get().split(', ', 1)[-1].strip(), '%B %d, %Y').date(),
            'stats': {},
        }
        for box in boxes:
            box.css('tbody')
            rows = box.css('tr')
            for row in rows:
                row = BS(row.get(), 'html.parser')
                try:
                   identity = row.find('th').find('a').get('href').split('/')[-1].split('.')[0].strip()
                   game_data['stats'][identity] = {
                        'name': row.find('th').find('a').get_text(),
                        'id': identity,
                        'minutes': int(row.find_all('td')[0].get_text()),
                        'fg': int(row.find_all('td')[1].get_text()),
                        'fga': int(row.find_all('td')[2].get_text()),
                        '2p': int(row.find_all('td')[4].get_text()),
                        '2pa': int(row.find_all('td')[5].get_text()),
                        '3p': int(row.find_all('td')[7].get_text()),
                        '3pa': int(row.find_all('td')[8].get_text()),
                        'ft': int(row.find_all('td')[10].get_text()),
                        'fta': int(row.find_all('td')[11].get_text()),
                        'orb': int(row.find_all('td')[13].get_text()),
                        'drb': int(row.find_all('td')[14].get_text()),
                        'reb': int(row.find_all('td')[15].get_text()),
                        'ast': int(row.find_all('td')[16].get_text()),
                        'stl': int(row.find_all('td')[17].get_text()),
                        'blk': int(row.find_all('td')[18].get_text()),
                        'tov': int(row.find_all('td')[19].get_text()),
                        'fls': int(row.find_all('td')[20].get_text()),
                        'pts': int(row.find_all('td')[21].get_text()),
                    }
                except (AttributeError, ValueError):
                    continue
        yield game_data