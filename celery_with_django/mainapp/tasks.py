from celery import shared_task
from django_celery_beat.models import PeriodicTask


@shared_task(bind=True)
def test_func(self):
    # opprations
    for i in range(10):
        print(i)

    return "Done"
