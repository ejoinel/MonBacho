# -*- coding: utf-8 -*-

from datetime import datetime
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
from django.contrib import messages
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.messages import constants as message_constants
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.template import loader
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as super_login
from django.contrib.auth import logout as super_logout

from MonBacho.settings import DEFAULT_FROM_EMAIL
from MonBacho.forms import LoginForm, UserForm, CreateExamForm, UploadFileForm, AccountResetPassword, BaseFileFormSet
from MonBacho.models import User, DocumentFile, Exam

import FORM_PROPERTIES

MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger', }


#@login_required(login_url='/login')
def home(request):
    return render_to_response('home.html', {'current_date_time': datetime.now()})
    # if 'logged_user_id' in request.session:
    #     logged_user_id = request.session['logged_user_id']
    #     logged_user = authenticate(id=logged_user_id)
    #     return render_to_response('home.html', {'current_date_time': datetime.now(), 'logged_user': logged_user})
    # else:
    #     return HttpResponseRedirect('/login')



def logout(request):
    super_logout(request)
    return HttpResponseRedirect('/login')



def reset_password(request):

    # Test si le fomulaire a été envoyé
    if request.method == "POST":
        form = AccountResetPassword(request.POST)
        context = {'form': form}

        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)

            if users:
                # the password verified for the user
                user = users[0]
                if user.is_active:
                    subject = FORM_PROPERTIES.PASSWORD_RESET_SUBJECT.decode('utf8')
                    subject = subject.replace("site_name", "MonBacho")
                    new_password = User.objects.make_random_password(length=6)
                    print new_password
                    user.set_password(new_password)
                    dict_values = {'email': user.email, 'site_name': 'MBacho', 'user': user, 'password': new_password}
                    email_template_name = 'account/password_reset_email.html'
                    email = loader.render_to_string(email_template_name, dict_values)
                    if send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False):
                        msg = FORM_PROPERTIES.PASSWORD_RESET.decode('utf8')
                        msg = msg.replace("user", user.email)
                        messages.add_message(request, messages.SUCCESS, msg)
                        user.save()
                        return HttpResponseRedirect('/login')
                    else:
                        msg = FORM_PROPERTIES.PASSWORD_NOT_SENT.decode('utf8')
                        messages.add_message(request, messages.ERROR, msg)
                        return render_to_response(template_name='account/resetpassword.html', context=context,
                                                  context_instance=RequestContext(request))
                else:
                    msg = FORM_PROPERTIES.FORM_LOGIN_NOT_ACTIVE.decode('utf8')
                    messages.add_message(request, messages.ERROR, msg)
                    return render_to_response(template_name='account/resetpassword.html', context=context,
                                              context_instance=RequestContext(request))
            else:
                msg = FORM_PROPERTIES.FORM_USER_NOT_FOUND.decode('utf8')
                messages.add_message(request, messages.ERROR, msg)
                return render_to_response(template_name='account/resetpassword.html', context=context,
                                          context_instance=RequestContext(request))
        else:
            context = {'form': form}
            return render_to_response(template_name='account/resetpassword.html', context=context,
                                      context_instance=RequestContext(request))
    else:
        form = AccountResetPassword()
        context = {'form': form}
        return render_to_response(template_name='account/resetpassword.html', context=context,
                                  context_instance=RequestContext(request))



def login(request):

    # Test si le fomulaire a été envoyé
    if request.method == "POST":
        form = LoginForm(request.POST)
        context = {'form': form}

        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = authenticate(email=email, password=password)

            if user:
                # the password verified for the user
                if user.is_active:
                    super_login(request, user)
                    msg = FORM_PROPERTIES.WELCOME_MSG.decode('utf8')
                    msg = msg.replace("user", user.nickname)
                    messages.add_message(request, messages.SUCCESS, msg)
                    request.session['logged_user_id'] = user.id
                    return HttpResponseRedirect('/home')
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
            msg = FORM_PROPERTIES.FORM_LOGIN_FAILED
            messages.add_message(request, messages.WARNING, msg)
            return render_to_response(template_name='login.html', context=context,
                                      context_instance=RequestContext(request))
    else:
        form = LoginForm()
        context = {'form': form}
        return render_to_response(template_name='login.html', context=context,
                                  context_instance=RequestContext(request))


@login_required(login_url='/login')
def createexam(request):

    # Creation du formulaire + upload des images
    doc_form = CreateExamForm(auto_id=True)

    # Création du formset avec n itération : extra=2
    file_form_set = modelformset_factory(DocumentFile, form=UploadFileForm, extra=3)

    # Récupération du formulaire géré par le mécanisme formset
    #formset = sortedfilesform()

    if request.method == "POST":

        doc_form = CreateExamForm(request.POST)
        post_files_formset = file_form_set(request.POST, request.FILES, queryset=DocumentFile.objects.none())

        if doc_form.is_valid() and post_files_formset.is_valid():
            new_doc = Exam(level=doc_form.cleaned_data['level'], matter=doc_form.cleaned_data['matter'],
                           school=doc_form.cleaned_data['school'], year_exam=doc_form.cleaned_data['year_exam'],
                           mock_exam=doc_form.cleaned_data['mock_exam'])
            new_doc.user = request.user
            new_doc.user_id = request.user.id
            new_doc.save()
            #list_files = files_form.save(commit=False)
            for form in post_files_formset.cleaned_data:
                image = form['file_value']
                description = form['description']
                doc_file = DocumentFile(document=new_doc, file_value=image, description=description)
                doc_file.save()

        return HttpResponseRedirect('/login')
    else:
        context = {'doc_form': doc_form, 'file_form_set': file_form_set, }
        return render(request, 'createexam.html', context)



def register(request):

    if request.method == "POST":
        form = UserForm(request.POST)
        form_values = {'form': form}
        error_form = False

        if form.is_valid():
            if 'nickname' in form.cleaned_data:
                nickname = form.cleaned_data['nickname']
            else:
                nickname = form.cleaned_data['email'].split("@")[0]
            mail = form.cleaned_data['email']

            if form.cleaned_data['password1'] != form.cleaned_data['password2']:
                error_form = True
                messages.add_message(request, messages.WARNING,
                                     FORM_PROPERTIES.FORM_MSG_PASSWORD_NO_MATCHING)

            # les speudo et mail sont uniques
            nb_nickname = len(User.objects.filter(nickname=nickname))
            if nb_nickname > 0:
                nickname = "{}_{}".format(nickname, nb_nickname + 1)

            if len(User.objects.filter(email=mail)) > 0:
                error_form = True
                messages.add_message(request, messages.WARNING,
                                     FORM_PROPERTIES.FORM_MAIL_USED)

            if error_form:
                return render_to_response('register.html', form_values,
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

            return render_to_response('register.html', form_values, context_instance=RequestContext(request))

    else:
        form = UserForm()
        form_values = {'form': form}
        return render_to_response('register.html', form_values, context_instance=RequestContext(request))
