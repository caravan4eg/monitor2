# django_project/celery.py
import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
app = Celery('django_project')
 
app.config_from_object('django.conf:settings', namespace='CELERY')
 
app.autodiscover_tasks()
 
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# --------------------------------------------------------------------
# Periodic task: run scrapy spider
# --------------------------------------------------------------------

app.conf.beat_schedule = {

    'Run Scrapy QuotesSpider': {
        'task': 'django_app.tasks.crawl',
        'schedule': crontab(minute=0, hour='*/3'),
                    # crontab(),  # every minute, 
                    # crontab(minute='*/15'),  # every 15 minutes
    },

}

# --------------------------------------------------------------------