#-*- coding: utf-8 -*-

from forms import LoginForm
from forms import CreateUserForm
from datetime import datetime
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


def welcome( request ):
    return render_to_response( 'welcome.html', {'current_date_time':datetime.now()} )



def login( request ):

    # Test si le fomulaire a été envoyé
    if ( request.method == "POST" ):
        form = LoginForm( request.POST )
        c = {'form': form}
        if form.is_valid():
            return HttpResponseRedirect( '/welcome' )
        else:
            return render_to_response( 'login.html', c,
                                       context_instance=RequestContext( request ) )
    else:
        form = LoginForm()
        c = {'form': form}
        return render_to_response( 'login.html', c, context_instance=RequestContext( request ) )



def register( request ):

    if len( request.GET ) < 0:
        form = CreateUserForm( request.GET )
        c = {'form': form}
        if form.is_valid():
            form.save( commit=True )
            return HttpResponseRedirect( '/register' )
        else:
            return render_to_response( 'register.html', c,
                                       context_instance=RequestContext( request ) )

    else:
        form = CreateUserForm()
        return render_to_response ( 'register.html', {'form': form} )

