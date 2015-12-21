#-*- coding: utf-8 -*-

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from MonBacho.models import User, Exam

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
    #remember = forms.BooleanField(label="Se souvenir de moi?")

    helper = FormHelper()
    helper.form_id = 'login-form'
    helper.form_show_labels = False
    helper.add_input(Submit('login', 'Connexion', css_class='btn btn-success btn-block'))
    #helper.layout(PrependedText('field_1', '@', placeholder="username"))

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

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'mot de passe'}),
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'confirmer le mot de passe'}),
                                label="Password")

    helper = FormHelper()
    helper.form_id = 'register-form'
    helper.form_show_labels = False
    helper.add_input(Submit('register', "S'inscrire", css_class='form-control btn btn-login'))

    class Meta:
        model = User
        fields = ('sex', 'email', 'password1', 'password2', 'lastname', 'firstname', 'birth_date', 'school')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['lastname'].widget = forms.TextInput(attrs={'placeholder': 'Nom'})
        self.fields['firstname'].widget = forms.TextInput(attrs={'placeholder': 'Prénom'})
        self.fields['birth_date'].widget = forms.DateInput(format='%d/%m/%Y',
                                                           attrs={'placeholder': 'Date de naissance jj/mm/YYYY'})

    def clean(self):

        cleaned_data = super(UserForm, self).clean()
        email = cleaned_data.get("email")
        nickname = cleaned_data.get("nickname")

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
