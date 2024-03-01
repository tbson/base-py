import os

from django.urls import include, path

app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = (
    path(
        "basic-auth/",
        include("module.auth.useacse.basic_auth.urls", namespace="basic_auth"),
    ),
    path(
        "common-auth/",
        include("module.auth.usecase.common_auth.urls", namespace="common_auth"),
    ),
)
