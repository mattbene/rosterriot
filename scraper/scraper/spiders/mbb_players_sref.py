import scrapy
from bs4 import BeautifulSoup as BS


class MbbPlayersSrefSpider(scrapy.Spider):
    name = "mbb_players_sref"
    allowed_domains = ["sports-reference.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.MbbPlayersSrefPipeline': 400
        }
    }
    start_urls = ["https://www.sports-reference.com/cbb/schools/"]
    

    def parse(self, response):
        table = response.css('#NCAAM_schools').css('tbody')
        for row in table.css('tr')[50:]: # SCRIPT LIMITOR HERE
            try:
                school_data = {
                    f"{row.css('td')[0].attrib['data-stat']}": row.css('td')[0].css('a::text').get().strip(),
                    "href": row.css('td')[0].css('a').attrib['href'],
                    f"{row.css('td')[1].attrib['data-stat']}": row.css('td::text')[0].get().strip(),
                    f"{row.css('td')[2].attrib['data-stat']}": int(row.css('td::text')[1].get().strip()),
                    f"{row.css('td')[3].attrib['data-stat']}": int(row.css('td::text')[2].get().strip()),
                }
                if school_data['year_max'] < 2024:
                    continue
                else:
                    yield scrapy.Request(f"https://sports-reference.com{school_data['href']}2024.html", callback=self.parse_team, meta=dict(href=school_data['href']))
            except IndexError:
                continue
    
    def parse_team(self, response):
        team_data = {
            'team': (response.meta['href'].split('/')[-3].strip(), 2024),
            'coach': None,
            'roster': {},
        }
        info = response.css('#info')
        for p in info.css('p'):
            try:
                if p.css('strong::text').get() == 'Coach:':
                    team_data['coach'] = p.css('a::text').get()
                else:
                    continue
            except:
                continue
        roster = BS(response.css('#roster').css('tbody').get(), 'html.parser')
        for row in roster.find_all('tr'):
            try:
                number = int(row.find_all('td')[0].get_text().strip())
            except:
                number = None
            try:
                position = row.find_all('td')[2].get_text().strip()
                if position == '':
                    position = None
            except:
                position = None
            try:
                ayear = row.find_all('td')[1].get_text().strip()
                if ayear == '':
                    ayear = None
            except:
                ayear = None
            try:
                height = round(float(row.find_all('td')[3].get_text().strip().split('-')[0]) + (float(row.find_all('td')[3].get_text().strip().split('-')[1]) / 12), 3)
            except:
                height = None
            try:
                weight = row.find_all('td')[4].get_text().strip()
            except:
                weight = None
            try:
                hometown = row.find_all('td')[5].get_text().strip()
                if hometown == '':
                    hometown = None
            except:
                hometown = None
            try:
                high_school = row.find_all('td')[6].get_text().strip()
                if high_school == '':
                    high_school = None
            except:
                high_school = None
            try:
                top100 = row.find_all('td')[7].get_text().strip()
                if top100 == '':
                    top100 = None
            except:
                top100 = None

            team_data['roster'][f"{row.find('a')['href'].rsplit('/', 1)[-1].split('.')[0].strip()}"]  = {
                'name': row.find('th').get_text().strip(),
                'sref_id': row.find('a')['href'].rsplit('/', 1)[-1].split('.')[0].strip(),
                'number': number,
                'class': ayear,
                'position': position,
                'height': height,
                'weight': weight,
                'hometown': hometown,
                'high_school': high_school,
                'top100': top100,
            }
        yield team_data