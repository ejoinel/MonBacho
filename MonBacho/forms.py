#-*- coding: utf-8 -*-

from django import forms
from MonBacho.models import student

import FORM_PROPERTIES
import ERROR_TXT

class LoginForm( forms.Form ):

    email = forms.EmailField( label=FORM_PROPERTIES.FORM_EMAIL,
                              max_length=30, widget=forms.EmailInput )

    password = forms.CharField( label=FORM_PROPERTIES.FORM_PASSWORD,
                                widget=forms.PasswordInput, max_length=30 )

    def clean( self ):
        cleaned_data = super ( LoginForm, self ).clean()
        email = cleaned_data.get( "email" )
        password = cleaned_data.get( "password" )

        # Vérifie que les deux champs sont valides
        if email and password:
            if password != "sesame" or email != "ejoinel@yahoo.fr":
                raise forms.ValidationError( ERROR_TXT.ERROR_EMAIL_PASSWORD_BAD )
        return cleaned_data



class CreateStudentForm( forms.ModelForm ):

    def __init__( self, *args, **kwargs ):
        super( CreateStudentForm, self ).__init__( *args, **kwargs )

        self.fields['name'].label = FORM_PROPERTIES.FORM_NAME
        #self.fields['sex'].label = FORM_PROPERTIES.FORM_SEXE
        self.fields['lastname'].label = FORM_PROPERTIES.FORM_LASTNAME
        self.fields['mail'].label = FORM_PROPERTIES.FORM_EMAIL
        self.fields['password'].label = FORM_PROPERTIES.FORM_PASSWORD
        self.fields['school'].label = FORM_PROPERTIES.FORM_SCHOOL
        self.fields['nickname'].label = FORM_PROPERTIES.FORM_NICKNAME

    class Meta:
        model = student
        exclude = ( 'phone_number', 'birth_date', 'sex', 'grade' )
