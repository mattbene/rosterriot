import scrapy


class TestProxySpider(scrapy.Spider):
    name = "test_proxy"
    allowed_domains = ["whatismyip.com"]
    start_urls = ["https://whatismyip.com"]

    def parse(self, response):
        info = response.css('#ip-info')
        yield {
            'ipv4': info.css('a.#ipv4::attr(href)').get(),
            'location': info.css('span.#geo::text').get(),
            'isp': info.css('span.#isp::text').get(),
        }
