#-*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.contrib import admin
from MonBacho.views import login, home, register, createexam, reset_password

admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home),
    url(r'^home', home),
    url(r'^login$', login),
    url(r'^register$', register),
    url(r'^createexam$', createexam),
    url(r'^account/reset_password', reset_password, name="reset_password"),
]
