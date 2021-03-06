# -*- coding: utf-8 -*-

import FORM_PROPERTIES

from django.forms.formsets import formset_factory
from forms import LoginForm, UserForm, CreateExamForm, UploadFileForm
from datetime import datetime
from MonBacho.models import User
from django.contrib import messages
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.messages import constants as message_constants
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger', }


@login_required(login_url='/login')
def home(request):
    if 'logged_user_id' in request.session:
        logged_user_id = request.session['logged_user_id']
        logged_user = authenticate(id=logged_user_id)
        return render_to_response('home.html', {'current_date_time': datetime.now(), 'logged_user': logged_user})
    else:
        return HttpResponseRedirect('/login')



def logout(request):
    logout(request)
    return HttpResponseRedirect('/login')



def login(request):

    # Test si le fomulaire a été envoyé
    if request.method == "POST":
        form = LoginForm(request.POST)
        context = {'form': form,}

        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = authenticate(email=email, password=password)

            if user:
                # the password verified for the user
                if user.is_active:
                    login(request, user)
                    msg = FORM_PROPERTIES.WELCOME_MSG.decode('utf8')
                    msg = msg.replace("user", user.nickname)
                    messages.add_message(request, messages.SUCCESS, msg)
                    return HttpResponseRedirect('/login')
                    request.session['logged_user_id'] = user.id
                else:
                    messages.add_message(request, messages.WARNING,
                                         FORM_PROPERTIES.FORM_LOGIN_NOT_ACTIVE)
                    return render_to_response(template_name='login.html', context=context,
                                              context_instance=RequestContext(request))
            else:
                msg = FORM_PROPERTIES.FORM_LOGIN_FAILED

                messages.add_message(request, messages.WARNING, msg)
                return render_to_response(template_name='login.html', context=context,
                                          context_instance=RequestContext(request))
    else:
        form = LoginForm()
        context = {'form': form,}
        return render_to_response(template_name='login.html', context=context,
                                  context_instance=RequestContext(request))


@login_required(login_url='/login')
def createexam(request):

    # Creation du formulaire + upload des images
    form = CreateExamForm(auto_id=True)

    # Création du formset avec n itération : extra=2
    sortedfilesform = formset_factory(UploadFileForm, extra=3)

    # Récupération du formulaire géré par le mécanisme formset
    formset = sortedfilesform()
    if request.method == "POST":
        form = CreateExamForm(request.POST)

        if form.is_valid():
            print("Super")
        else:
            print("Mauvais")
    else:
        context = {'form': form, 'sortedForm': formset, }
        return render(request, 'createexam.html', context)


def register(request):

    if request.method == "POST":
        form = UserForm(request.POST)
        c = {'form': form}
        error_form = False

        if form.is_valid():
            if 'nickname' in form.cleaned_data:
                nickname = form.cleaned_data['nickname']
            else:
                nickname = form.cleaned_data['email'].split("@")[0]
            mail = form.cleaned_data['email']

            if form.cleaned_data['password1'] != form.cleaned_data['password2']:
                error_form = True
                form._errors['password1'].append('Some field is blank')
                messages.add_message(request, messages.WARNING,
                                     FORM_PROPERTIES.FORM_MSG_PASSWORD_NO_MATCHING)

            # les speudo et mail sont uniques
            nb_nickname = len(User.objects.filter(nickname=nickname))
            if nb_nickname > 0:
                nickname = "{}_{}".format(nickname, nb_nickname+1)

            if len(User.objects.filter(email=mail)) > 0:
                error_form = True
                messages.add_message(request, messages.WARNING,
                                     FORM_PROPERTIES.FORM_MAIL_USED)

            if error_form:
                return render_to_response('register.html', c,
                                          context_instance=RequestContext(request))

            msg = FORM_PROPERTIES.FORM_MSG_ACCOUNT_CREATED.decode('utf8')
            msg = msg.replace("name", nickname)

            stored_user = form.save(commit=False)
            stored_user.password = make_password(form.cleaned_data['password1'])
            stored_user.nickname = nickname
            stored_user.save()
            messages.add_message(request, messages.SUCCESS, msg)

            return HttpResponseRedirect('/login')
        else:
            messages.add_message(request, messages.ERROR,
                                 FORM_PROPERTIES.FORM_MSG_ACCOUNT_ERROR)

            return render_to_response('register.html', c,
                                      context_instance=RequestContext(request))

    else:
        form = UserForm()
        c = {'form': form}
        return render_to_response('register.html', c,
                                  context_instance=RequestContext(request))
