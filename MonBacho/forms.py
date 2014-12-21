#-*- coding: utf-8 -*-

from django import forms

import FORM_PROPERTIES

class LoginForm(forms.Form):

    email = forms.EmailField(label=FORM_PROPERTIES.FORM_EMAIL)
    password = forms.CharField(label=FORM_PROPERTIES.FORM_PASSWORD, widget=forms.PasswordInput)
