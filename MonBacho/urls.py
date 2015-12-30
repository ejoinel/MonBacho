#-*- coding: utf-8 -*-

import MonBacho

from django.conf.urls import url, include
from views import login, home, register, createexam
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', 'MonBacho.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', MonBacho.views.home),
    url(r'^home', MonBacho.views.home),
    url(r'^login$', MonBacho.views.login),
    url(r'^register$', MonBacho.views.register),
    url(r'^createexam$', MonBacho.views.createexam),
]
