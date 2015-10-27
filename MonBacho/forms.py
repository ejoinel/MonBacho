#-*- coding: utf-8 -*-

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML
from crispy_forms.bootstrap import ( PrependedText,
                                    PrependedAppendedText, FormActions )

from MonBacho.models import user, exam

import FORM_PROPERTIES
import ERROR_TXT



# Formulaire login
class LoginForm( forms.Form ):

    email = forms.EmailField( label=FORM_PROPERTIES.FORM_EMAIL,
                              max_length=30, widget=forms.EmailInput( attrs={'placeholder': 'entrer@login.com'} ),
                              required=True )

    password = forms.CharField( label=FORM_PROPERTIES.FORM_PASSWORD,
                                required=True, widget=forms.PasswordInput( attrs={'placeholder': 'Mot de passe'} ), max_length=30 )
    #remember = forms.BooleanField( label="Se souvenir de moi?" )

    helper = FormHelper()
    helper.form_id = 'login-form'
    helper.form_show_labels = False
    helper.add_input( Submit( 'login', 'Connexion', css_class='btn btn-success btn-block' ) )
    #helper.layout( PrependedText( 'field_1', '@', placeholder="username" ) )

    def clean( self ):
        cleaned_data = super ( LoginForm, self ).clean()
        email = cleaned_data.get( "email" )
        password = cleaned_data.get( "password" )

        # Vérifie que les deux champs sont valides
        if email and password:
            if len( user.objects.filter( password=password, mail=email ) != 1 ):
                raise forms.ValidationError( ERROR_TXT.ERROR_EMAIL_PASSWORD_BAD )
        return cleaned_data



# Fomulaire création d'utilisateur
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

    helper = FormHelper()
    helper.form_id = 'register-form'
    helper.form_show_labels = False
    helper.add_input( Submit( 'register', "S'inscrire", css_class='form-control btn btn-login' ) )

    class Meta:
        model = user
        exclude = ( 'phone_number', 'birth_date', 'sex', 'creation_date',
                    'slug', 'modification_date' )

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



class UploadFileForm( forms.Form ):
    file = forms.FileField()



#Formulaire création d'examen
class CreateExamForm( forms.ModelForm ):

    class Meta:
        model = exam
        exclude = ( "slug", "user", "nb_views", "name", "status",
                    "creation_date", "deletion_date" )
