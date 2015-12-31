#-*- coding: utf-8 -*-

import MonBacho

from django.conf.urls import url, include
from views import login, home, register, createexam
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', 'MonBacho.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', MonBacho.views.home),
    url(r'^home', MonBacho.views.home),
    url(r'^login$', MonBacho.views.login),
    url(r'^register$', MonBacho.views.register),
    url(r'^recover/(?P<signature>.+)/$', views.recover_done, name='password_reset_sent'),
    url(r'^recover/$', views.recover, name='password_reset_recover'),
    url(r'^reset/done/$', views.reset_done, name='password_reset_done'),
    url(r'^reset/(?P<token>[\w:-]+)/$', views.reset,
        name='password_reset_reset'),
]
