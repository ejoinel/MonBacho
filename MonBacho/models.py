#-*- coding: utf-8 -*-

#import DATABASE_CONF
from django.db import models


PERSON_SEX_CHOISE = ( 
    ( '0', 'Mr' ),
    ( '1', 'Mme' ),
    ( '2', 'Mlle' )
 )



class classlevel( models.Model ):
    class Meta:
        db_table = 'classlevel'

    name = models.CharField( max_length=30 )
    sub_category = models.CharField( max_length=30 )

    def __unicode__( self ):
        if self.sub_category:
            return self.name + "(" + self.sub_category + ")"
        else:
            return self.name



class school( models.Model ):
    class Meta:
        db_table = 'school'

    name = models.CharField( max_length=100 )

    def __unicode__( self ):
        return self.name



class classtopic( models.Model ):
    class Meta:
        db_table = 'classtopic'

    name = models.CharField( max_length=30 )

    def __unicode__( self ):
        return self.name



class user( models.Model ):

    class Meta:
        db_table = 'user'

    slug = models.SlugField( max_length=100 )
    school = models.OneToOneField( school, null=True, blank=True )
    sex = models.IntegerField( choices=PERSON_SEX_CHOISE, default=0 )
    firstname = models.CharField( max_length=30 )
    lastname = models.CharField( max_length=30 )
    nickname = models.CharField( max_length=30 )
    mail = models.EmailField( max_length=72 )
    password = models.CharField( max_length=100 )
    nb_points = models.IntegerField( default=0 )
    birth_date = models.DateField( default=None, blank=True, null=True )
    creation_date = models.DateTimeField( auto_now_add=True, blank=True )
    modification_date = models.DateTimeField( auto_now_add=True, blank=True )

    def __unicode__( self ):
        return self.nickname + " (" + self.nickname + ") " + self.school.name



class document( models.Model ):
    class Meta:
        db_table = 'document'

    slug = models.SlugField( max_length=100 )
    user = models.ForeignKey( user )
    level = models.ForeignKey( classlevel )
    school = models.ForeignKey( school )
    nb_views = models.IntegerField( default=0 )
    name = models.CharField( max_length=100 )
    status = models.IntegerField( default=-1 )
    creation_date = models.DateTimeField( auto_now_add=True )
    deletion_date = models.DateTimeField( auto_now_add=True )

    def __unicode__( self ):
        return self.name + " (" + self.status + ") " + self.school.name



class image( models.Model ):
    class Meta:
        db_table = 'image'
    file_path = models.CharField( max_length=100 )
    document = models.ForeignKey( document, null=True, blank=True, default=None )



class exam ( document ):

    class Meta:
        db_table = 'exam'

    matter = models.ForeignKey( classtopic )

    def __unicode__( self ):
        return self.name + " " + self.matter



class correction ( document ):

    class Meta:
        db_table = 'correction'

    exam = models.ForeignKey( exam )
    text = models.TextField( max_length=1024 )

    def __unicode__( self ):
        return "{} correction du sujet {}".format( self.id, exam.id )



class read ( models.Model ):

    class Meta:
        db_table = 'read'
    read_date = models.DateTimeField( auto_now_add=True )
    document = models.ForeignKey( document, related_name='read_document' )
    user = models.ForeignKey( user, related_name='read_user' )

    def __unicode__( self ):
        return self.user.name + " - " + self.document.name + " (" + self.read_date + ")"



class submit ( models.Model ):

    class Meta:
        db_table = 'submit'
    submit_date = models.DateTimeField( auto_now_add=True )
    document = models.ForeignKey( document, related_name='submit_document' )
    user = models.ForeignKey( user, related_name='submit_user' )

    def __unicode__( self ):
        return self.user.name + " - " + self.document.name + " (" + self.submit_date + ")"



class comment ( models.Model ):

    class Meta:
        db_table = 'comment'
    comment_date = models.DateTimeField( auto_now_add=True )
    comment = models.TextField( max_length=512 )
    document = models.ForeignKey( document, related_name='comment_document' )
    user = models.ForeignKey( user, related_name='comment_user' )

    def __unicode__( self ):
        return self.user.name + " - " + self.document.name + " - " + self.comment + " (" + self.comment_date + ")"

