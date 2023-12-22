import scrapy
from datetime import datetime, date
from zoneinfo import ZoneInfo


class MbbGamesAmEspnSpider(scrapy.Spider):
    name = "mbb_games_am_espn"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.MbbGamesAmEspnPipeline': 400
        }
    }
    allowed_domains = ["espn.com"]
    start_urls = [f"https://www.espn.com/mens-college-basketball/scoreboard/_/date/{datetime.strftime(date.today(),'%Y%m%d')}/seasontype/2/group/50"]

    def parse(self, response):
        for game in response.css('section.Scoreboard'):
            yield scrapy.Request(f"https://www.espn.com/mens-college-basketball/game/_/gameId/{game.attrib['id']}", callback=self.parse_game, cb_kwargs=dict(game_id=game.attrib['id']))
            
            
    
    def parse_game(self, response, game_id):
        game_info = response.css('section.Card.GameInfo')
        team_info = response.css('div.Gamestrip__TeamContent')
        try:
            home_team_id = int(team_info[1].css('a::attr(href)').get().split('/')[-2])
        except:
            home_team_id = team_info[1].css('h2::text').get()
        try:
            away_team_id = int(team_info[0].css('a::attr(href)').get().split('/')[-2])
        except:
             away_team_id = team_info[0].css('h2::text').get()
        try:
            spread = float(game_info.css('div.n8.GameInfo__BettingItem.line::text').getall()[2].split(' ')[-1].strip())
        except:
            spread = None
        try:
            favorite = game_info.css('div.n8.GameInfo__BettingItem.line::text').getall()[2].split(' ')[0].strip()
        except:
            favorite = None
        try:
            total = float(game_info.css('div.n8.GameInfo__BettingItem.ou::text').getall()[-1].strip())
        except:
            total = None
        try:
            location = str(game_info.css('span.Location__Text::text').getall()[0].strip() + ', ' + game_info.css('span.Location__Text::text').getall()[-2].strip())
        except:
            location = None
        yield {
            'id': int(game_id),
            'date': date.today(),
            'home_team_id': home_team_id,
            'away_team_id': away_team_id,
            'time': datetime.time(datetime.strptime(str(game_info.css('span::text').get().split(', ', 1)[0]).strip(), '%I:%M %p')).replace(tzinfo=ZoneInfo('America/New_York')),
            'location': location,
            'arena': game_info.css('div.n6::text').get(),
            'spread': spread,
            'total': total,
            'favorite': favorite,
            }