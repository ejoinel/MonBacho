#-*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm, extras
from django.forms.formsets import BaseFormSet
from passwords.fields import PasswordField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, HTML
from crispy_forms.bootstrap import PrependedText, Field
from multiupload.fields import MultiFileField

from MonBacho.models import User, Exam, DocumentFile

import FORM_PROPERTIES
import ERROR_TXT

EXAM_YEAR_CHOICES = ('2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009')

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
        PrependedText('email', '<span class="fa fa-user fa-lg"></span>', placeholder="Email"),
        PrependedText('password', '<span class="fa fa-lock fa-lg"></span>', placeholder="Mot de passe"))

    helper.add_input(Submit('login', 'Connexion', css_class='btn btn-success btn-block'))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        # Vérifie que les deux champs sont valides
        if email and password:
            if len(User.objects.filter(email=email)) != 1:
                raise forms.ValidationError(ERROR_TXT.ERROR_EMAIL_PASSWORD_BAD)
        return cleaned_data



# Formulaire login
class AccountResetPassword(forms.Form):

    email = forms.EmailField(label=FORM_PROPERTIES.FORM_EMAIL,
                             max_length=30,
                             widget=forms.EmailInput(attrs={'placeholder': 'entrer@login.com'}),
                             required=True)

    helper = FormHelper()
    helper.form_id = 'reset-password-form'
    helper.form_show_labels = False
    helper.layout = Layout(PrependedText('email', '@', placeholder="email"))

    helper.add_input(Submit('reset_password', 'Réinitialiser', css_class='btn btn-success btn-block'))

    def clean(self):
        cleaned_data = super(AccountResetPassword, self).clean()
        email = cleaned_data.get("email")

        # Vérifie que les deux champs sont valides
        if email:
            if len(User.objects.filter(email=email)) != 1:
                raise forms.ValidationError(ERROR_TXT.ERROR_EMAIL_PASSWORD_BAD)
        return cleaned_data



# Fomulaire création d'utilisateur
class UserForm(forms.ModelForm):

    email = forms.EmailField(label=FORM_PROPERTIES.FORM_EMAIL,
                             max_length=30,
                             widget=forms.EmailInput(attrs={'placeholder': 'entrez@login.com'}))

    password1 = PasswordField(widget=forms.PasswordInput(attrs={'placeholder': 'mot de passe'}),
                              label="Password")
    password2 = PasswordField(widget=forms.PasswordInput(),
                              help_text="Confimer le mot de passe",
                              label="Password")

    birth_date = forms.DateField(help_text="Cette information restera privée")

    helper = FormHelper()
    helper.form_id = 'register-form'
    helper.form_show_labels = False
    helper.layout = Layout(PrependedText('sex', '', ''),
                           PrependedText('email', '<span class="fa fa-user fa-lg"></span>', placeholder="Email"),
                           PrependedText('password1', '<span class="fa fa-lock fa-lg fa-lg"></span>', placeholder="Mot de passe"),
                           PrependedText('password2', '<span class="fa fa-lock fa-lg fa-lg"></span>', placeholder="Confirmer"),
                           PrependedText('last_name', '<span class="fa fa-tag fa-lg"></span>', placeholder="Nom(s)"),
                           PrependedText('first_name', '<span class="fa fa-tag fa-lg"></span>', placeholder="Prenom(s)"),
                           PrependedText('birth_date', '<span class="fa fa-calendar fa-lg"></span>', placeholder="dd/MM/YYYY"),
                           PrependedText('school', '', css_class='selectpicker'),)
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


class UploadFileForm(ModelForm):

    description = forms.CharField(max_length=30)

    image = forms.ImageField(label='Image')

    helper = FormHelper()
    helper.form_id = 'file-input'
    helper.form_show_labels = False
    helper.layout = Layout(
        PrependedText('description', '<span class="fa fa-commenting fa-lg"></span>', placeholder="Ex: N° page"),
        PrependedText('image', "", placeholder=""))
    #helper.layout.insert(1, HTML("<input type='file' class='file' multiple data-show-upload='false' data-show-caption='true'>"))

    class Meta:
        model = DocumentFile
        fields = ['description', 'image']



# formset des fichiers
class BaseFileFormSet(BaseFormSet):

    def clean(self):

        if any(self.errors):
            return

        descriptions = []
        duplicates = False

        for form in self.forms:
            description = form.cleaned_data['description']

            if description:
                if description in descriptions:
                    duplicates = True
                descriptions.append(description)

            if duplicates:
                raise forms.ValidationError('Les descriptions des fichiers doivent être unique.', code='duplicate_links')



# Formulaire création d'examen
class CreateExamForm(forms.ModelForm):

    first_files = MultiFileField( min_num=1, max_num=3, max_file_size=1024 * 1024 * 5 )
    second_files = MultiFileField( min_num=0, max_num=4, max_file_size=1024 * 1024 * 5 )
    helper = FormHelper()
    helper.form_id = 'CreateExam'
    helper.form_show_labels = False
    helper.layout = Layout(
        PrependedText("matter", "", ""),
        PrependedText("level", "<small class='text-warning'>Selectionner la classe. </small>", ""),
        PrependedText("school", "<pre><small>Selectionner l\'établissement. </small></pre>", css_class="selectpicker"),
        PrependedText("year_exam", ""),
        PrependedText("mock_exam", ""),
        PrependedText("first_files", ""),
        PrependedText("second_files", ""))

    class Meta:
        model = Exam
        exclude = ("slug", "user", "nb_views", "name", "status", "creation_date", "deletion_date")