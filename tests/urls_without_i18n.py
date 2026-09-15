"""A URLconf with no ``set_language`` route, for the graceful-degradation tests."""

from django.contrib import admin
from django.urls import path

urlpatterns = [path("admin/", admin.site.urls)]
