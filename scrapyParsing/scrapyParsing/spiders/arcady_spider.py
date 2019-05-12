import scrapy
from scrapy import Request
from ..items import ScrapyparsingItem


class ArcadySpider(scrapy.Spider):
    name = "arcady"

    def start_requests(self):
        start_urls = ["https://letyshops.com/shops?page=1"]
        for url in start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        items = ScrapyparsingItem()
        names = response.xpath('//a[@class="b-teaser__inner"]//div[@class="b-teaser__title"]//text()').extract()
        for name in names:
            items["name"] = name
            yield items

    def get_discounts(self):
        pass