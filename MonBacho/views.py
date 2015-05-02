# -*- coding: utf-8 -*-

import FORM_PROPERTIES

from forms import LoginForm
from datetime import datetime
from django.contrib import messages
from forms import CreateStudentForm
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.messages import constants as message_constants


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
            messages.add_message( request, messages.SUCCESS, 'We did it!' )
            return HttpResponseRedirect( '/welcome' )
        else:
            return render_to_response( 'login.html', c,
                                       context_instance=RequestContext( request ) )
    else:
        form = LoginForm()
        c = {'form': form}
        return render_to_response( 'login.html', c,
                                   context_instance=RequestContext( request ) )



def register( request ):

    if ( request.method == "POST" ):
        form = CreateStudentForm( request.POST )
        c = {'form': form}
        if form.is_valid():
            nickname = form.data['nickname']
            msg = FORM_PROPERTIES.FORM_MSG_ACCOUNT_CREATED.decode( 'utf8' )
            msg = msg.replace( "name", nickname )

            form.save( commit=True )
            messages.add_message( request, messages.SUCCESS, msg )

            return HttpResponseRedirect( '/login' )
        else:
            messages.add_message( request, messages.ERROR,
                                  FORM_PROPERTIES.FORM_MSG_ACCOUNT_ERROR )

            return render_to_response( 'register.html', c,
                                       context_instance=RequestContext( request ) )

    else:
        form = CreateStudentForm()
        c = {'form': form}
        return render_to_response( 'register.html', c,
                                   context_instance=RequestContext( request ) )

