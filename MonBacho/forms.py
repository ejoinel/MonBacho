#-*- coding: utf-8 -*-

from django import forms
from passwords.fields import PasswordField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django.core.validators import validate_email
from crispy_forms.bootstrap import (PrependedText)

from MonBacho.models import User, Exam
from django.conf import settings
from django.db.models import Q
from .utils import get_user_model

import FORM_PROPERTIES
import ERROR_TXT


# Formulaire login
class LoginForm(forms.Form):

    email = forms.EmailField(label=FORM_PROPERTIES.FORM_EMAIL,
                             max_length=30,
                             widget=forms.EmailInput(attrs={'placeholder': 'entrer@login.com'}),
                             required=True)

    password = forms.CharField(label=FORM_PROPERTIES.FORM_PASSWORD,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
                               max_length=30)

    helper = FormHelper()
    helper.form_id = 'login-form'
    helper.form_show_labels = False
    helper.layout = Layout(
        PrependedText('email', '@', placeholder="email"),
        PrependedText('password', '**', placeholder="mot de passe"))

    helper.add_input(Submit('login', 'Connexion', css_class='btn btn-success btn-block'))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        # Vérifie que les deux champs sont valides
        if email and password:
            if len(User.objects.filter(password=password, mail=email)) != 1:
                raise forms.ValidationError(ERROR_TXT.ERROR_EMAIL_PASSWORD_BAD)
        return cleaned_data


# Fomulaire création d'utilisateur
class UserForm(forms.ModelForm):

    email = forms.EmailField(label=FORM_PROPERTIES.FORM_EMAIL,
                             max_length=30,
                             widget=forms.EmailInput(attrs={'placeholder': 'entrez@login.com'}))

    password1 = PasswordField(widget=forms.PasswordInput(attrs={'placeholder': 'mot de passe'}),
                              label="Password")
    password2 = PasswordField(widget=forms.PasswordInput(attrs={'placeholder': 'confirmer le mot de passe'}),
                              label="Password")

    helper = FormHelper()
    helper.form_id = 'register-form'
    helper.form_show_labels = False
    helper.add_input(Submit('register', "S'inscrire", css_class='form-control btn btn-login'))

    class Meta:
        model = User
        fields = ('sex', 'email', 'password1', 'password2', 'last_name', 'first_name', 'birth_date', 'school')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['last_name'].widget = forms.TextInput(attrs={'placeholder': 'Nom'})
        self.fields['first_name'].widget = forms.TextInput(attrs={'placeholder': 'Prénom'})
        self.fields['birth_date'].widget = forms.DateInput(format='%d/%m/%Y',
                                                           attrs={'placeholder': 'Date de naissance jj/mm/YYYY'})

    def clean(self):

        cleaned_data = super(UserForm, self).clean()
        email = cleaned_data.get("email")
        nickname = cleaned_data.get("nickname")

        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(FORM_PROPERTIES.FORM_MSG_PASSWORD_NO_MATCHING)

        # Vérifie que les deux champs sont valides
        if len(User.objects.filter(email=email)) > 0:
            raise forms.ValidationError(FORM_PROPERTIES.FORM_MAIL_USED)

        if len(User.objects.filter(nickname=nickname)) > 0:
            raise forms.ValidationError(FORM_PROPERTIES.FORM_NICKNAME_USED)
        return cleaned_data

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UploadFileForm(forms.Form):
    file = forms.FileField()


# Formulaire création d'examen
class CreateExamForm(forms.ModelForm):

    class Meta:
        model = Exam
        exclude = ("slug", "user", "nb_views", "name", "status",
                   "creation_date", "deletion_date")



class PasswordRecoveryForm(forms.Form):
    username_or_email = forms.CharField()

    error_messages = {
        'not_found': ("Sorry, this user doesn't exist."),
    }

    def __init__(self, *args, **kwargs):
        self.case_sensitive = kwargs.pop('case_sensitive', True)
        search_fields = kwargs.pop('search_fields', ('username', 'email'))
        super(PasswordRecoveryForm, self).__init__(*args, **kwargs)

        message = ("No other fields than username and email are supported "
                   "by default")
        if len(search_fields) not in (1, 2):
            raise ValueError(message)
        for field in search_fields:
            if field not in ['username', 'email']:
                raise ValueError(message)

        labels = {
            'username': ('Username'),
            'email': ('Email'),
            'both': ('Username or Email'),
        }
        User = get_user_model()  # noqa
        if getattr(User, 'USERNAME_FIELD', 'username') == 'email':
            self.label_key = 'email'
        elif len(search_fields) == 1:
            self.label_key = search_fields[0]
        else:
            self.label_key = 'both'
        self.fields['username_or_email'].label = labels[self.label_key]

    def clean_username_or_email(self):
        username = self.cleaned_data['username_or_email']
        cleaner = getattr(self, 'get_user_by_%s' % self.label_key)
        self.cleaned_data['user'] = user = cleaner(username)

        user_is_active = getattr(user, 'is_active', True)
        recovery_only_active_users = getattr(settings,
                                             'RECOVER_ONLY_ACTIVE_USERS',
                                             False)

        if recovery_only_active_users and not user_is_active:
            raise forms.ValidationError(("Sorry, inactive users can't "
                                         "recover their password."))

        return username

    def get_user_by_username(self, username):
        key = 'username__%sexact' % ('' if self.case_sensitive else 'i')
        User = get_user_model()
        try:
            user = User._default_manager.get(**{key: username})
        except User.DoesNotExist:
            raise forms.ValidationError(self.error_messages['not_found'],
                                        code='not_found')
        return user

    def get_user_by_email(self, email):
        validate_email(email)
        key = 'email__%sexact' % ('' if self.case_sensitive else 'i')
        User = get_user_model()
        try:
            user = User._default_manager.get(**{key: email})
        except User.DoesNotExist:
            raise forms.ValidationError(self.error_messages['not_found'],
                                        code='not_found')
        return user

    def get_user_by_both(self, username):
        key = '__%sexact'
        key = key % '' if self.case_sensitive else key % 'i'
        f = lambda field: Q(**{field + key: username})
        filters = f('username') | f('email')
        User = get_user_model()
        try:
            user = User._default_manager.get(filters)
        except User.DoesNotExist:
            raise forms.ValidationError(self.error_messages['not_found'],
                                        code='not_found')
        except User.MultipleObjectsReturned:
            raise forms.ValidationError("Unable to find user.")

        return user


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='New password (confirm)',
        widget=forms.PasswordInput,
    )

    error_messages = {'password_mismatch': "The two passwords didn't match.",}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data['password2']
        if not password1 == password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password1'])
        if commit:
            get_user_model()._default_manager.filter(pk=self.user.pk).update(
                password=self.user.password,
            )
        return self.user

