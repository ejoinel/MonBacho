#-*- coding: utf-8 -*-

from django.conf.urls import url, include

from views import login, welcome, register
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'MonBacho.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url( r'^$', welcome ),
    url( r'^welcome$', welcome ),
    url( r'^login$', login ),
    url( r'^register$', register ),
    url( r'^admin', include( admin.site.urls ) ),
]
