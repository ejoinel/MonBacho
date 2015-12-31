# -*- coding: utf-8 -*-

import FORM_PROPERTIES
import datetime

from django.forms.formsets import formset_factory
from forms import LoginForm, UserForm, CreateExamForm, UploadFileForm
from MonBacho.models import User
from django.contrib import messages
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.messages import constants as message_constants
from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.contrib.sites.models import Site
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core import signing
from django.core.mail import send_mail
from django.template import loader
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.debug import sensitive_post_parameters
from django.views import generic
from django.http import Http404
from django.conf import settings

from .forms import PasswordRecoveryForm, PasswordResetForm
from .signals import user_recovers_password
from .utils import get_user_model, get_username

try:
    from django.contrib.sites.requests import RequestSite
except ImportError:
    from django.contrib.sites.models import RequestSite

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
        return render_to_response('home.html', {'current_date_time': datetime.datetime.now(), 'logged_user': logged_user})
    else:
        return HttpResponseRedirect('/login')



def userlogout(request):
    logout(request)
    return HttpResponseRedirect('/login')



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
                nickname = "{}_{}".format(nickname, nb_nickname + 1)

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



# Reset password views
class SaltMixin(object):
    salt = 'password_recovery'
    url_salt = 'password_recovery_url'


def loads_with_timestamp(value, salt):
    """Returns the unsigned value along with its timestamp, the time when it
    got dumped."""
    try:
        signing.loads(value, salt=salt, max_age=-1)
    except signing.SignatureExpired as e:
        age = float(str(e).split('Signature age ')[1].split(' >')[0])
        timestamp = timezone.now() - datetime.timedelta(seconds=age)
        return timestamp, signing.loads(value, salt=salt)


class RecoverDone(SaltMixin, generic.TemplateView):
    template_name = 'password_reset/reset_sent.html'

    def get_context_data(self, **kwargs):
        ctx = super(RecoverDone, self).get_context_data(**kwargs)
        try:
            ctx['timestamp'], ctx['email'] = loads_with_timestamp(
                self.kwargs['signature'], salt=self.url_salt,
            )
        except signing.BadSignature:
            raise Http404
        return ctx
recover_done = RecoverDone.as_view()


class Recover(SaltMixin, generic.FormView):
    case_sensitive = True
    form_class = PasswordRecoveryForm
    template_name = 'password_reset/recovery_form.html'
    success_url_name = 'password_reset_sent'
    email_template_name = 'password_reset/recovery_email.txt'
    email_subject_template_name = 'password_reset/recovery_email_subject.txt'
    search_fields = ['username', 'email']

    def get_success_url(self):
        return reverse(self.success_url_name, args=[self.mail_signature])

    def get_context_data(self, **kwargs):
        kwargs['url'] = self.request.get_full_path()
        return super(Recover, self).get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(Recover, self).get_form_kwargs()
        kwargs.update({
            'case_sensitive': self.case_sensitive,
            'search_fields': self.search_fields,
        })
        return kwargs

    def get_site(self):
        if Site._meta.installed:
            return Site.objects.get_current()
        else:
            return RequestSite(self.request)

    def send_notification(self):
        context = {
            'site': self.get_site(),
            'user': self.user,
            'username': get_username(self.user),
            'token': signing.dumps(self.user.pk, salt=self.salt),
            'secure': self.request.is_secure(),
        }
        body = loader.render_to_string(self.email_template_name,
                                       context).strip()
        subject = loader.render_to_string(self.email_subject_template_name,
                                          context).strip()
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
                  [self.user.email])

    def form_valid(self, form):
        self.user = form.cleaned_data['user']
        self.send_notification()
        if (
            len(self.search_fields) == 1 and
            self.search_fields[0] == 'username'
        ):
            # if we only search by username, don't disclose the user email
            # since it may now be public information.
            email = self.user.username
        else:
            email = self.user.email
        self.mail_signature = signing.dumps(email, salt=self.url_salt)
        return super(Recover, self).form_valid(form)
recover = Recover.as_view()


class Reset(SaltMixin, generic.FormView):
    form_class = PasswordResetForm
    token_expires = 3600 * 48  # Two days
    template_name = 'password_reset/reset.html'
    success_url = reverse_lazy('password_reset_done')

    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

        try:
            pk = signing.loads(kwargs['token'], max_age=self.token_expires,
                               salt=self.salt)
        except signing.BadSignature:
            return self.invalid()

        self.user = get_object_or_404(get_user_model(), pk=pk)
        return super(Reset, self).dispatch(request, *args, **kwargs)

    def invalid(self):
        return self.render_to_response(self.get_context_data(invalid=True))

    def get_form_kwargs(self):
        kwargs = super(Reset, self).get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(Reset, self).get_context_data(**kwargs)
        if 'invalid' not in ctx:
            ctx.update({
                'username': get_username(self.user),
                'token': self.kwargs['token'],
            })
        return ctx

    def form_valid(self, form):
        form.save()
        user_recovers_password.send(
            sender=get_user_model(),
            user=form.user,
            request=self.request
        )
        return redirect(self.get_success_url())
reset = Reset.as_view()


class ResetDone(generic.TemplateView):
    template_name = 'password_reset/recovery_done.html'


reset_done = ResetDone.as_view()