#-*- coding: utf-8 -*-

from django import forms
from MonBacho.models import user

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
            if len( user.objects.filter( password=password, mail=email ) != 1 ):
                raise forms.ValidationError( ERROR_TXT.ERROR_EMAIL_PASSWORD_BAD )
        return cleaned_data



class UserForm( forms.ModelForm ):

    password = forms.CharField( widget=forms.PasswordInput() )

    mail = forms.EmailField( label=FORM_PROPERTIES.FORM_EMAIL,
                              max_length=30, widget=forms.EmailInput )

    def __init__( self, *args, **kwargs ):
        super( UserForm, self ).__init__( *args, **kwargs )

        self.fields['firstname'].label = FORM_PROPERTIES.FORM_NAME
        #self.fields['sex'].label = FORM_PROPERTIES.FORM_SEXE
        self.fields['lastname'].label = FORM_PROPERTIES.FORM_LASTNAME
        self.fields['mail'].label = FORM_PROPERTIES.FORM_EMAIL
        self.fields['password'].label = FORM_PROPERTIES.FORM_PASSWORD
        self.fields['school'].label = FORM_PROPERTIES.FORM_SCHOOL
        self.fields['nickname'].label = FORM_PROPERTIES.FORM_NICKNAME

    class Meta:
        model = user
        exclude = ( 'phone_number', 'birth_date', 'sex', 'creation_date', 'slug', 'modification_date' )

    def clean( self ):

        cleaned_data = super ( UserForm, self ).clean()
        mail = cleaned_data.get( "mail" )
        nickname = cleaned_data.get( "nickname" )

        # Vérifie que les deux champs sont valides
        if ( len( user.objects.filter( mail=mail ) ) > 0 ):
            raise forms.ValidationError( FORM_PROPERTIES.FORM_MAIL_USED )

        if ( len( user.objects.filter( nickname=nickname ) ) > 0 ):
            raise forms.ValidationError( FORM_PROPERTIES.FORM_NICKNAME_USED )
        return cleaned_data
