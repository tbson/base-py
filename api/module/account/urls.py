import os

from django.urls import include, path

app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = (path("user/", include("module.account.urls", namespace="user")),)
