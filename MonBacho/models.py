# -*- coding: utf-8 -*-

# import DATABASE_CONF
from django.db import models



PERSON_SEX_CHOICE = (('0', 'Mr'), ('1', 'Mme'), ('2', 'Mlle'))

EXAM_YEAR_CHOICES = ('2015', '2014', '2014', '2013', '2012', '2011', '2010')
# year = forms.ChoiceField(choices=[(x, x) for x in range(1900, 2000)], required=False)



class ClassLevel( models.Model ):
    class Meta:
        db_table = 'ClassLevel'

    name = models.CharField( max_length=30 )
    sub_category = models.CharField( max_length=30 )



    def __unicode__(self):
        if self.sub_category:
            return self.name + "(" + self.sub_category + ")"
        else:
            return self.name



class School( models.Model ):
    class Meta:
        db_table = 'School'

    name = models.CharField( max_length=100 )



    def __unicode__(self):
        return self.name



class ClassTopic( models.Model ):
    class Meta:
        db_table = 'ClassTopic'

    name = models.CharField( max_length=30 )



    def __unicode__(self):
        return self.name



class User( models.Model ):

    class Meta:
        db_table = 'User'

    slug = models.SlugField( max_length=100 )
    school = models.OneToOneField( School, null=True, blank=True )
    sex = models.IntegerField( choices=PERSON_SEX_CHOICE, default=0 )
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



class Document( models.Model ):
    class Meta:
        db_table = 'Document'

    slug = models.SlugField( max_length=100 )
    user = models.ForeignKey( User )
    level = models.ForeignKey( ClassLevel )
    school = models.ForeignKey( School )
    nb_views = models.IntegerField( default=0 )
    name = models.CharField( max_length=100 )
    status = models.IntegerField( default=-1 )
    creation_date = models.DateTimeField( auto_now_add=True )
    deletion_date = models.DateTimeField( auto_now_add=True )



    def __unicode__(self):
        return self.name + " (" + self.status + ") " + self.school.name



class Image( models.Model ):
    class Meta:
        db_table = 'Image'

    file_path = models.CharField( max_length=100 )
    document = models.ForeignKey( Document, null=True, blank=True, default=None )



class Exam( Document ):
    class Meta:
        db_table = 'Exam'

    matter = models.ForeignKey( ClassTopic )



    def __unicode__(self):
        return self.name + " " + self.matter



class Correction( Document ):
    class Meta:
        db_table = 'Correction'

    exam = models.ForeignKey( Exam )
    text = models.TextField( max_length=1024 )



    def __unicode__(self):
        return "{} correction du sujet {}".format( self.id, Exam.id )



class Read( models.Model ):
    class Meta:
        db_table = 'Read'

    read_date = models.DateTimeField( auto_now_add=True )
    document = models.ForeignKey( Document, related_name='read_document' )
    user = models.ForeignKey( User, related_name='read_user' )



    def __unicode__(self):
        return self.user.name + " - " + self.document.name + " (" + self.read_date + ")"



class Submit( models.Model ):
    class Meta:
        db_table = 'Submit'

    submit_date = models.DateTimeField( auto_now_add=True )
    document = models.ForeignKey( Document, related_name='submit_document' )
    user = models.ForeignKey( User, related_name='submit_user' )



    def __unicode__(self):
        return self.user.name + " - " + self.document.name + " (" + self.submit_date + ")"



class Comment( models.Model ):
    class Meta:
        db_table = 'Comment'

    comment_date = models.DateTimeField( auto_now_add=True )
    comment = models.TextField( max_length=512 )
    document = models.ForeignKey( Document, related_name='comment_document' )
    user = models.ForeignKey( User, related_name='comment_user' )



    def __unicode__(self):
        return self.user.name + " - " + self.document.name + " - " + self.comment + " (" + self.comment_date + ")"
