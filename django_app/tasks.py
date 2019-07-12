# django_app/tasks.py
from __future__ import absolute_import, unicode_literals
 
import os
import subprocess
from celery import task, shared_task
 
 
#------------------------------------------------------------------------------
# run spider from tasks
#------------------------------------------------------------------------------
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy_project.spiders.icetrade import IceSpiderSpider
 
@shared_task
def crawl():
    print('***** The crawl task is starting... *****')
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(IceSpiderSpider)
    process.start()
