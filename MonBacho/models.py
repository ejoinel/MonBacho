# -*- coding: utf-8 -*-

# import DATABASE_CONF
import os
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

PERSON_SEX_CHOICE = ((0, 'Mr'), (1, 'Mme'), (2, 'Mlle'))

FILE_TYPE = (
    (1, 'image'),
    (2, 'pdf'),
    (3, 'video'),
)

EXAM_TYPE = (
    (1, 'real'),
    (2, 'mock'),
)

DOCUMENT_STATUS = (
    (1, 'new'),
    (2, 'cleared'),
    (3, 'deleted'),
)

EXAM_YEAR_CHOICES = (
    (2016, '2016'),
    (2015, '2015'),
    (2014, '2014'),
    (2013, '2013'),
    (2012, '2012'),
    (2011, '2011'),
)



class ClassLevel( models.Model ):
    class Meta:
        db_table = 'ClassLevel'

    name = models.CharField( max_length=30 )
    sub_category = models.CharField( max_length=30 )

    def __unicode__( self ):
        if self.sub_category:
            return self.name + "(" + self.sub_category + ")"
        else:
            return self.name



class School( models.Model ):
    class Meta:
        db_table = 'School'

    name = models.CharField( max_length=100 )

    def __unicode__( self ):
        return self.name



class ClassTopic( models.Model ):
    class Meta:
        db_table = 'ClassTopic'

    name = models.CharField( max_length=30 )

    def __unicode__( self ):
        return self.name



class UserManager( BaseUserManager ):
    def create_user( self, email, password, **kwargs ):
        user = self.model( email=self.normalize_email( email ), is_active=True, **kwargs )
        user.set_password( password )
        user.save( )
        return user

    def create_superuser( self, email, password, **kwargs ):
        user = self.model( email=email, is_staff=True, is_superuser=True, is_active=True, **kwargs )
        user.set_password( password )
        user.save( )
        return user



class User( AbstractBaseUser, PermissionsMixin ):
    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'MonBacho'
        db_table = "User"

    slug = models.SlugField( max_length=100 )
    nickname = models.SlugField( max_length=20, null=True, blank=True )
    first_name = models.SlugField( max_length=30, default=None, null=True )
    last_name = models.SlugField( max_length=30, default=None, null=True )
    school = models.ForeignKey( School, null=True, blank=True )
    sex = models.IntegerField( choices=PERSON_SEX_CHOICE, default=0 )
    nb_points = models.IntegerField( default=0 )
    birth_date = models.DateField( default=None, blank=True, null=True )
    email = models.EmailField( 'email address', unique=True, max_length=254, db_index=True )
    date_joined = models.DateTimeField( 'date joined', default=timezone.now )
    is_active = models.BooleanField( 'active', default=True )
    is_admin = models.BooleanField( default=False )
    is_staff = models.BooleanField( default=False )
    receive_newsletter = models.BooleanField( 'receive newsletter', default=True )

    objects = UserManager( )

    def get_full_name( self ):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip( )

    def get_short_name( self ):
        return self.first_name

    def __unicode__( self ):
        return self.email



class Document( models.Model ):
    class Meta:
        db_table = 'Document'

    slug = models.SlugField( max_length=50 )
    user = models.ForeignKey( User )
    document_type = "generic"
    level = models.ForeignKey( ClassLevel, null=False, default=1 )
    school = models.ForeignKey( School, null=False, default=1 )
    nb_views = models.IntegerField( default=0 )
    name = models.CharField( max_length=100 )
    matter = models.ForeignKey( ClassTopic, null=False, default=1 )
    status = models.IntegerField( choices=DOCUMENT_STATUS, default=1 )
    creation_date = models.DateTimeField( auto_now_add=True )
    deletion_date = models.DateTimeField( null=True, default=None )

    def __unicode__( self ):
        return self.name + " (" + str( self.status ) + ") " + self.school.name



def upload_function( instance, filename ):
    import settings
    from helper import helper


    my_helper = helper( )
    ext = filename.split( '.' )[-1]
    filename = "{}_{}.{}".format( instance.document.id, instance.temp_id, ext )
    document_path = "{}/{}/{}/{}/{}/{}"
    doc_level = "{}{}".format( instance.document.level.name, instance.document.level.sub_category )

    document_path = document_path.format( instance.document.document_type, instance.document.school.name, doc_level,
                                          instance.document.matter.name, instance.document.year_exam,
                                          instance.document.id )

    parsed_document_path = "{}/{}".format( my_helper.remove_accents_spaces( document_path ), filename )

    return os.path.join( settings.MEDIA_ROOT + '/{}'.format( parsed_document_path ) )



class DocumentFile( models.Model ):
    class Meta:
        db_table = 'DocumentFile'

    description = models.CharField( max_length=50, null=True )
    image = models.ImageField( upload_to=upload_function, verbose_name='image', )
    document = models.ForeignKey( Document, default=None )

    def __unicode__( self ):
        return self.file_path



class Exam( Document ):
    class Meta:
        db_table = 'Exam'

    year_exam = models.IntegerField( choices=EXAM_YEAR_CHOICES, default='2016' )
    mock_exam = models.IntegerField( choices=EXAM_TYPE, default=1 )
    document_type = "exam"

    def __unicode__( self ):
        return self.name + " " + self.matter

    def save( self, *args, **kwargs ):
        if not self.id:
            # Newly created object, so set slug
            slug_text = "{} {} {} {} {}".format( self.school.name, self.level.name,
                                                 self.level.sub_category, self.year_exam, self.mock_exam )
            self.slug = self.name = slugify( slug_text )

        super( Exam, self ).save( *args, **kwargs )



class Correction( Document ):
    class Meta:
        db_table = 'Correction'

    exam = models.ForeignKey( Exam )
    text = models.TextField( max_length=1024 )
    document_type = "correction"

    def __unicode__( self ):
        return _( u"{} correction du sujet {}".format( self.id, Exam.id ) )



class Read( models.Model ):
    class Meta:
        db_table = 'Read'

    read_date = models.DateTimeField( auto_now_add=True )
    document = models.ForeignKey( Document, related_name='read_document' )
    user = models.ForeignKey( User, related_name='read_user' )

    def __unicode__( self ):
        return self.user.email + " - " + self.document.name + " (" + str( self.read_date ) + ")"



class Submit( models.Model ):
    class Meta:
        db_table = 'Submit'

    submit_date = models.DateTimeField( auto_now_add=True )
    document = models.ForeignKey( Document, related_name='submit_document' )
    user = models.ForeignKey( User, related_name='submit_user' )

    def __unicode__( self ):
        return "{} {} {}".format( self.user.email, self.document.name, self.submit_date )



class Comment( models.Model ):
    class Meta:
        db_table = 'Comment'

    comment_date = models.DateTimeField( auto_now_add=True )
    comment = models.TextField( max_length=512 )
    document = models.ForeignKey( Document, related_name='comment_document' )
    user = models.ForeignKey( User, related_name='comment_user' )

    def __unicode__( self ):
        return "{} {} {} {}".format( self.user.email, self.document.name, self.comment, self.comment_date )
