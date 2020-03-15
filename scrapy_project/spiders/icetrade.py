# scrapy_project/spiders/icetrade.py
# TODO: improove proxy, user agent and headers rotation or increase delay
# TODO: check get request real headers and addr which tracks server

import scrapy
from scrapy import signals
from datetime import date
import scrapy_project.params

from scrapy_project.items import TenderItem

from time import sleep
import random
from random import randint

import logging


RESULT_PAGE_PRIORITY = 0
PRODUCT_PAGE_PRIORITY = 100


class IceSpiderSpider(scrapy.Spider):
    name = "icetrade"
    allowed_domains = ['icetrade.by']
    today_is = date.today().strftime("%d.%m.%Y")
    custom_settings = {

                    'CONCURRENT_REQUESTS': 1,
                    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
                    'FEED_FORMAT': 'csv',
                    'FEED_URI': f'output/{today_is}_icetrade_tenders.csv',
                }

    proxies = {}

    def get_proxy_meta(self):
        meta = {}
        proxy = min(self.proxies, key=self.proxies.get)
        self.proxies[proxy] += 1
        meta['download_slot'] = proxy
        # meta["cookie_jar"] = proxy
        return meta

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(IceSpiderSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def start_requests(self):
        # https://free-proxy-list.net/
        # https://www.us-proxy.org/
        yield scrapy.Request(url="https://www.us-proxy.org/",
                             callback=self.parse_proxy)
        self.crawler.stats._stats["used_proxies"] = self.proxies

    def spider_closed(self, spider):
        self.crawler.stats._stats["used_proxies_count"] = len(list(self.proxies))
        print('~~~~~~~~~~~~ Spider "%s" closed ~~~~~~~~~~' % spider.name)

    def parse_proxy(self, response):
        print('~~~~~~~~~~~~ Getting proxy list ~~~~~~~~~~')
        for row in response.xpath('//table/tbody/tr'):
            # proxy_item = ProxyItem()
            row_data = row.xpath('.//td/text()').getall()
            # proxy_item['ip'] = row.xpath('.//td/text()')[0].get()
            # proxy_item['port'] = row.xpath('.//td/text()')[1].get()

            # because can be too few elite proxy
            # host_port = row_data[0]+':'+row_data[1]
            # self.proxies[host_port] = 0
            # print(f'~~~~~~~~~~~~ Proxy URL: {host_port}  ~~~~~~~~~~')

            if ('elite proxy' in row_data): #or ('anonymous' in row_data): #
                host_port = row_data[0]+':'+row_data[1]
                self.proxies[host_port] = 0
                print(f'Elite proxy URL: {host_port}')



        if len(list(self.proxies)) > 0:
            yield scrapy.Request(url=scrapy_project.params.url_pattern.format(str(1)),
                                 meta=self.get_proxy_meta(),
                                 callback=self.parse,
                                 priority=PRODUCT_PAGE_PRIORITY,
                                 # errback=self.err_back,
                                 # headers=self.get_ua_header(),
                            )

        print(f'~~~~~~~~~~~~ Total proxies: {len(self.proxies)}  ~~~~~~~~~~')


    def parse(self, response):
        """ Get page url """
        sleep(randint(1,3))
        last_page = response.xpath('//div[@id="content"]/div[@class="paging"]/a[9]/text()').get().strip()

        for i in range(int(last_page)+1):
        # for i in range(1):  # scrape some pages for test, not all

            # request next page and callback to Parse page function
            logging.info(f'==========  Processing page: {str(i)}  ===========')
            sleep(randint(5, 10))
            yield scrapy.Request(
                                scrapy_project.params.url_pattern.format(str(i)),
                                meta=self.get_proxy_meta(),
                                callback=self.parse_page,
                                priority=RESULT_PAGE_PRIORITY
                                )

    def parse_page(self, response):
        """ Extract tender information """
        logging.info('~~~~~~~~~~~~ Start exrtacting data from page ~~~~~~~~~~')

        # item = {}
        for line in response.xpath('//*/tr[contains(@class, "rw")]'):
            item = TenderItem()
            item['number'] = line.xpath('.//td[4]/text()').get().strip()
            item['customer'] = line.xpath('.//td[2]/text()').get().strip()
            item['description'] = line.xpath('.//td[1]/a/text()').get().strip()
            item['price'] = line.xpath('.//td[5]/span/text()').get().strip()
            item['country'] = line.xpath('.//td[3]/text()').get().strip()
            item['url_addr'] = line.xpath('.//td[1]/a/@href').get()
            # change date format dd-mm-yyyy --> yyyy-mm-dd
            ddmmyyyy = line.xpath('.//td[6]/text()').get().strip()
            yyyymmdd = ddmmyyyy[6:] + "-" + ddmmyyyy[3:5] + "-" + ddmmyyyy[:2]
            item['deadline'] = yyyymmdd

            # self.logger.info('\n**** <parse_page>: scrapping tender <%s>:' % item['number'])
            yield item

        sleep(randint(1, 3))

        print('~~~~~~~~~~~~ Extracting ended. ~~~~~~~~~~')

    def err_back(self, failure):
        # Not finished/tested yet
        req = failure.request
        if "download_slot" in req.meta.keys():
            failed_proxy = req.meta["download_slot"]
            if failed_proxy in self.proxies.keys():
                del self.proxies[failed_proxy]  # delete invalid proxy
                req.meta = self.get_proxy_meta()  # get new proxy
                yield req
