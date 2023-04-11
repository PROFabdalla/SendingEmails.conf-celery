from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djcelery_proj.settings")

app = Celery("djcelery_proj")
app.conf.update(timezone="Africa/Cairo")

app.config_from_object(settings, namespace="CELERY")


# Celery Beat Settings
app.conf.beat_schedule = {
    "send-mail-every-day-at-8": {
        "task": "send_mail_app.tasks.send_mail_func",
        "schedule": crontab(hour=16, minute=45),  # send message every day at 4 pm
        # "schedule": 16.0,                             # send message every 16 second
        # "args" : (2,)                                 # # sended to task function
    }
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
