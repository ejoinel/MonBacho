#-*- coding: utf-8 -*-

from django.conf.urls import url
from views import welcome
from views import login

urlpatterns = [
    # Examples:
    # url(r'^$', 'MonBacho.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', welcome),
    url(r'^welcome$', welcome),
    url(r'^login$', login)
]
