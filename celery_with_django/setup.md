# setup celery with django and redis

## packages (set in INSTALLED_APPS)

    1- pip install celery
    2- pip install django-celery-beat

## commands to run celery

    # first run server

    # second in powershell to run worker that do the tasks
        celery -A djcelery_proj.celery worker --pool=solo -l info

    # third in powershell to run beat that do the tasks schedular
        celery -A djcelery_proj beat -l info

## ----------------------------------------------------------------------------------------------------------

## project core app

##### 1- setting.py

    CELERY_BROKER_URL = "redis://127.0.0.1:6379" # redis end_point
    CELERY_ACCEPT_CONTENT = ["application/json"]
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TASK_SERIALIZER = "json"
    CELERY_TIMEZONE = "Africa/Cairo"

    CELERY_RESULT_BACKEND = "django-db"


    # ------- CELERY BEAT (scheduler tasks)  ----- #
    CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


    # ----------- SMTP ----------#
    # ----------- django email sitting ----------#
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = True
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_HOST_USER = "sending account"                # come from your google account
    EMAIL_HOST_PASSWORD = "google password"         # come from your (1-"google account manager" 2-"security" 3-"apps passwords")
    DEFAULT_FROM_EMAIL = "default from email"

##### 2- **init**.py

    from .celery import app as celery_app
    __all__ = ("celery_app",)

##### 3- celery.py

        from __future__ import absolute_import, unicode_literals
        import os
        from celery import Celery
        from django.conf import settings

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings")
        app = Celery("project_name")
        app.conf.update(timezone="Africa/Cairo")

        app.config_from_object(settings, namespace="CELERY")


        # Celery Beat Settings
        app.autodiscover_tasks()
        @app.task(bind=True)
        def debug_task(self):
            print(f"Request: {self.request!r}")

## ------------------------------------------------------------------------------------------

### end_points app (main_app)

##### 1 - tasks.py

    # ------- file has the tasks will action ------ #

        """
        from celery import shared_task

        @shared_task(bind=True)
        def test_func(self):
            # opprations like loops
        """

##### 2 - views.py

    # ---------- file has the end point (must have urls in urls.py) ----------- #

        """
        from .tasks import test_func
        from send_email_app.tasks import send_mail_func

        def test(request):
            test_func.delay()
            return HttpResponse("Done")

        def send_mail_to_all(request):
            send_mail_func.delay()
            return HttpResponse("Send")
        """

## ------------------------------------------------------------------------------------------

### send_mail app

##### 1 - tasks.py

        from django.contrib.auth import get_user_model
        from djcelery_proj import settings
        from celery import shared_task
        from django.core.mail import send_mail

        User = get_user_model()

        @shared_task(bind=True)
        def send_mail_func(self):
            users = User.objects.all()
            # opprations
            for user in users:
                mail_subject = "hi! celery testing"
                message = "i like celery till now !"
                to_email = user.email
                send_mail(
                    subject=mail_subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[to_email],
                    fail_silently=False,
                )
            return "Send"
