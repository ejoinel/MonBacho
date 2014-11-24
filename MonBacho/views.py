#-*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from datetime import datetime


def welcome(request):
    return render_to_response('welcome.html', {'current_date_time':datetime.now()})

def login(request):
    return render_to_response('login.html')