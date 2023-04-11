from django.shortcuts import render
from django.http import HttpResponse
from mainapp.tasks import test_func
from send_mail_app.tasks import send_mail_func
from django_celery_beat.models import PeriodicTask

# Create your views here.


def test(request):
    test_func.delay()
    return HttpResponse("Done")


def send_mail_to_all(request):
    send_mail_func.delay()
    return HttpResponse("Send")


def enable_periodic_task(request):
    periodic_task = PeriodicTask.objects.get(name="send-mail-every-day-at-8")
    periodic_task.enabled = True
    periodic_task.save()
    return HttpResponse("enable")


def del_periodic_task(request):
    periodic_task = PeriodicTask.objects.get(name="send-mail-every-day-at-8")
    # periodic_task.delete()
    periodic_task.enabled = False
    periodic_task.save()
    return HttpResponse("del")
