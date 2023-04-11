from django.urls import path
from mainapp.views import (
    test,
    send_mail_to_all,
    del_periodic_task,
    enable_periodic_task,
)

urlpatterns = [
    path("", test, name="test"),
    path("send/", send_mail_to_all, name="send_mail"),
    path("del/", del_periodic_task, name="delete_periodic_task"),
    path("enable/", enable_periodic_task, name="enable_periodic_task"),
]
