# -*- coding: utf-8 -*-
import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule


class GazpromSpiderSpider(scrapy.Spider):
    name = 'gazprom_spider'
    allowed_domains = ['belarus-tr.gazprom.ru']
    start_urls = ['https://belarus-tr.gazprom.ru/tenders/#1/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    def parse(self, response):
        print(response.body)
        # print(response.xpath('//*/tr[contains(@class, "odd" | "even")]'))

    def parse_item(self, response):
        item = {}

        # print(response.xpath('//*/tr[contains(@class, "odd" | "even")]'))

        # for line in response.xpath('//*/tr[contains(@class, "odd" | "even")]'):
        #     item['customer'] = line.xpath('.//td[3]/text()').get().strip()
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
