import scrapy
from scrapy import Request

from ..items import ScrapyparsingItem


class ArcadySpider(scrapy.Spider):
    name = "arcady"
    address = "https://letyshops.com/shops?page="

    def start_requests(self):
        start_urls = []
        for i in range(1,31):
            start_urls.append(self.address + i.__str__())
        for url in start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        items = ScrapyparsingItem()
        shops = response.xpath('//a[@class="b-teaser__inner"]')
        for i, shop in enumerate(shops):
            name = self.get_name(shop, i)
            url = self.get_url(shop, i)
            discount = self.get_discount(shop, i)
            label = self.get_label(shop, i)
            image = self.get_image(shop, i)
            yield {
                "name": name,
                "url": url,
                "discount": discount,
                "label": label,
                "image": image
            }

    def get_name(self, shop, i):
        name = shop.xpath('//div[@class="b-teaser__title"]//text()').extract()
        return name[i]

    def get_url(self, shop, i):
        url = shop.xpath('//a[@class="b-teaser__inner"]/@href').extract()
        return url[i]

    def get_discount(self, shop, i):
        index = i + 1
        discount = shop.xpath(
            '//div[@class="b-teaser"][' + index.__str__() + ']/a//span[@class="b-shop-teaser__cash"]/text()').get()
        if discount is None:
            discount = shop.xpath(
                '//div[@class="b-teaser"][' + index.__str__() + ']/a//span[@class="b-shop-teaser__new-cash"]/text()').get()
            print(discount)
            return discount
        return discount

    def get_label(self, shop, i):
        index = i + 1
        label = shop.xpath('//div[@class="b-teaser"]/a//span[@class="b-shop-teaser__label"]/text()')[-1].get()
        if label is None:
            label = shop.xpath(
                '//div[@class="b-teaser"]/a//span[@class="b-shop-teaser__label b-shop-teaser__label--red"]/text()')
            return label
        return label

    def get_image(self, shop, i):
        index = i + 1
        image = shop.xpath('//div[' + index.__str__() + ']//div[@class="b-teaser__cover"]/img/@src').extract()
        return image
