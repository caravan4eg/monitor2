import scrapy
# from django_app import models
# from scrapy_djangoitem import DjangoItem


class TenderItem(scrapy.Item):
    number = scrapy.Field()
    customer = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
    country = scrapy.Field()
    url_addr = scrapy.Field()
    deadline = scrapy.Field()
    # django_model = models.Tenders
