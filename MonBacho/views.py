# -*- coding: utf-8 -*-

import FORM_PROPERTIES

from forms import LoginForm
from datetime import datetime
from MonBacho.models import user
from django.contrib import messages
from forms import UserForm
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.messages import constants as message_constants
from __builtin__ import False
from django.contrib.auth.hashers import make_password


MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger', }



def welcome( request ):
    return render_to_response( 'welcome.html', {'current_date_time':datetime.now()} )



def login( request ):

    # Test si le fomulaire a été envoyé
    if ( request.method == "POST" ):
        form = LoginForm( request.POST )
        c = {'form': form}

        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            if( len( user.objects.filter( password=password, mail=email ) ) != 1 ):
                messages.add_message( request, messages.WARNING,
                                      FORM_PROPERTIES.FORM_LOGIN_FAILED )
                return render_to_response( 'login.html', c,
                                           context_instance=RequestContext( request ) )
            #user_connected = user.objects.get( password=password, mail=email ).nickname

            return HttpResponseRedirect( '/welcome' )
        else:
            msg = FORM_PROPERTIES.FORM_LOGIN_FAILED

            messages.add_message( request, messages.WARNING, msg )
            return render_to_response( 'login.html', c,
                                       context_instance=RequestContext( request ) )
    else:
        form = LoginForm()
        c = {'form': form}
        return render_to_response( 'login.html', c,
                                   context_instance=RequestContext( request ) )



def register( request ):

    if ( request.method == "POST" ):
        form = UserForm( request.POST )
        c = {'form': form}
        error_form = False

        if form.is_valid():

            nickname = form.cleaned_data['nickname']
            mail = form.cleaned_data['mail']

            # les speudo et mail sont uniques
            if ( len( user.objects.filter( nickname=nickname ) ) > 0 ):
                error_form = True
                messages.add_message( request, messages.WARNING,
                                      FORM_PROPERTIES.FORM_NICKNAME_USED )

            if ( len( user.objects.filter( mail=mail ) ) > 0 ):
                error_form = True
                messages.add_message( request, messages.WARNING,
                                      FORM_PROPERTIES.FORM_MAIL_USED )

            if error_form:
                return render_to_response( 'register.html', c,
                                           context_instance=RequestContext( request ) )

            msg = FORM_PROPERTIES.FORM_MSG_ACCOUNT_CREATED.decode( 'utf8' )
            msg = msg.replace( "name", nickname )

            stored_user = form.save( commit=False )
            stored_user.password = make_password( form.cleaned_data['password'] )
            stored_user.save()
            messages.add_message( request, messages.SUCCESS, msg )

            return HttpResponseRedirect( '/login' )
        else:
            messages.add_message( request, messages.WARNING,
                                  FORM_PROPERTIES.FORM_MSG_ACCOUNT_ERROR )

            return render_to_response( 'register.html', c,
                                       context_instance=RequestContext( request ) )

    else:
        form = UserForm()
        c = {'form': form}
        return render_to_response( 'register.html', c,
                                   context_instance=RequestContext( request ) )

