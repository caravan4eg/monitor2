# -*- coding: utf-8 -*-
import scrapy


class LukoilSpiderSpider(scrapy.Spider):
    name = 'lukoil_spider'
    allowed_domains = ['lukoil.ru']
    start_urls = ['https://lukoil.ru/Company/Tendersandauctions/Tenders/TendersofLukoilgroup?wid=widFAUvStA7tUSWn_q-AZhoGw']

    def parse(self, response):
        item = {}
        for line in response.xpath('//div[contains(@class, "panel-tender")]'):
            # item['number'] = line.xpath('.//span[contains(@data-bind, "text: Number")]/text()').get().strip()
            item['description'] = line.xpath('.//div[contains(@class, "panel-heading")]/h2/text()').get()
            # item['customer'] = line.xpath('.//span[contains(@data-bind, "text: Organization.Name")]/text()').get().strip()
            print(item['description'])
