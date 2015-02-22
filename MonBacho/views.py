#-*- coding: utf-8 -*-

from forms import LoginForm
from datetime import datetime
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response



def welcome(request):
    return render_to_response('welcome.html', {'current_date_time':datetime.now()})



def login(request):

    # Test si le fomulaire a été envoyé
    if (request.method == "POST"):
        form = LoginForm(request.POST)
        c = {'form': form}
        if form.is_valid():
            return HttpResponseRedirect('/welcome')
        else:
            return render_to_response('login.html', c, context_instance=RequestContext(request))
    else:
        form = LoginForm()
        c = {'form': form}
        return render_to_response('login.html', c, context_instance=RequestContext(request))
