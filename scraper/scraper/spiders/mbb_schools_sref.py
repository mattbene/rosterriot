import scrapy
from bs4 import BeautifulSoup as S


class MbbSchoolsSrefSpider(scrapy.Spider):
    name = "mbb_schools_sref"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.MbbSchoolsSrefPipeline': 300
        }
    }
    allowed_domains = ["sports-reference.com"]
    start_urls = ["https://sports-reference.com/cbb/schools/"]

    def parse(self, response):
        table = S(response.css('#NCAAM_schools').get(), 'html.parser')
        body = table.find('tbody')
        rows = body.find_all('tr')
        rows = [row for row in rows if 'class' not in row.attrs or row['class'][0] != 'thead']
        for row in rows:
            try: 
                tds = row.find_all('td')
                try:
                    if int(tds[3].get_text()) != 2024:
                        continue
                    else:
                        yield {
                            'school': tds[0].find('a').get_text().strip(),
                            'city': tds[1].get_text().split(', ')[0].strip(),
                            'state': tds[1].get_text().split(', ')[1].strip(),
                            'sref_id': tds[0].find('a').get('href').split('/')[-3].strip(),
                        }
                except ValueError:
                    continue

            except AttributeError:
                continue






            #yield {'row': row.find('td').get_text()}
           
