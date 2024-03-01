import os

from django.urls import include, path

app_name = os.getcwd().split(os.sep)[-1]

urlpatterns = (
    path("auth/", include("module.auth.urls", namespace="auth")),
    path("account/", include("module.account.urls", namespace="account")),
)
