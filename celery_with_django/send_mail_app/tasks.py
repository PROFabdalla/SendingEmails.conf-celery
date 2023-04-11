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
        print(to_email)
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=False,
        )

    return "Done"
