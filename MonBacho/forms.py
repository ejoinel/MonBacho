#-*- coding: utf-8 -*-

from django import forms

import FORM_PROPERTIES
import ERROR_TXT

class LoginForm(forms.Form):

    email = forms.EmailField(label=FORM_PROPERTIES.FORM_EMAIL,
                             max_length=30, widget=forms.EmailInput)

    password = forms.CharField(label=FORM_PROPERTIES.FORM_PASSWORD,
                               widget=forms.PasswordInput, max_length=30)

    def clean(self):
        cleaned_data = super (LoginForm, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        # Vérifie que les deux champs sont valides
        if email and password:
            if password != "sesame" or email != "ejoinel@yahoo.fr":
                raise forms.ValidationError(ERROR_TXT.ERROR_EMAIL_PASSWORD_BAD)
        return cleaned_data



class CreateUserForm(forms.Form):

    nickname = forms.EmailField(label=FORM_PROPERTIES.FORM_EMAIL,
                                max_length=30, widget=forms.EmailInput)

    email = forms.EmailField(label=FORM_PROPERTIES.FORM_EMAIL,
                             max_length=30, widget=forms.EmailInput)

    password = forms.CharField(label=FORM_PROPERTIES.FORM_PASSWORD,
                               widget=forms.PasswordInput, max_length=30)

    def clean(self):
        cleaned_data = super (CreateUserForm, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        # Vérifie que les deux champs sont valides
        if email and password:
            if password != "sesame" or email != "ejoinel@yahoo.fr":
                raise forms.ValidationError(ERROR_TXT.ERROR_EMAIL_PASSWORD_BAD)
        return cleaned_data
