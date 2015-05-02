#-*- coding: utf-8 -*-

import DATABASE_CONF
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

    def __unicode__( self ):
        return self.name



class school( models.Model ):
    class Meta:
        db_table = 'school'

    name = models.CharField( max_length=30 )

    def __unicode__( self ):
        return self.name



class schoolsubject( models.Model ):
    class Meta:
        db_table = 'schoolsubject'

    name = models.CharField( max_length=30 )

    def __unicode__( self ):
        return self.name



class user( models.Model ):

    class Meta:
        db_table = 'user'

    sex = models.IntegerField( choices=PERSON_SEX_CHOISE, default=0 )
    name = models.CharField( max_length=30 )
    lastname = models.CharField( max_length=30 )
    nickname = models.CharField( max_length=30 )
    birth_date = models.DateField( default=None, blank=True, null=True )
    mail = models.EmailField( max_length=30 )
    phone_number = models.CharField( max_length=20, blank=True, null=True )
    password = models.CharField( max_length=30 )
    school = models.ForeignKey( school )

    def __unicode__( self ):
        return self.nickname + " (" + self.nickname + ") " + self.school.name



class student( user ):

    class Meta:
        db_table = 'student'

    grade = models.ForeignKey( classlevel, default=DATABASE_CONF.DEFAULT_CLASSLEVEL )

    def __unicode__( self ):
        return self.nickname + "(" + self.nickname + ")"



class professor( user ):

    class Meta:
        db_table = 'professor'

    function = models.CharField( max_length=50 )

    def __unicode__( self ):
        return self.sex + " " + self.nickname + "(" + self.nickname + ")"



class correction( models.Model ):

    class Meta:
        db_table = 'correction'

    creation_date = models.DateField()
    fields = models.CharField( max_length=50 )

    def __unicode__( self ):
        return self.fields + " " + self.creation_date



class exam ( models.Model ):

    class Meta:
        db_table = 'exam'
    name = models.CharField( max_length=30 )
    creation_date = models.DateField()
    matter = models.ForeignKey( schoolsubject )
    corrections = models.ManyToManyField( 'correction', through='propose', related_name='correction' )
    users = models.ManyToManyField( 'user', through='submit', related_name='submit' )

    def __unicode__( self ):
        return self.name + " " + self.matter



class examperiod ( models.Model ):

    class Meta:
        db_table = 'examperiod'
    name = models.CharField( max_length=30 )
    mock_exam = models.BooleanField( default=True )
    examens = models.ManyToManyField( 'exam', through='concern', related_name='exam' )

    def __unicode__( self ):
        return self.name + " " + self.is_real_examen



class classgrades ( models.Model ):

    class Meta:
        db_table = 'classgrade'
    name = models.CharField( max_length=30 )
    creation_date = models.DateField()
    school = models.ForeignKey( school )
    classlevel = models.ForeignKey( classlevel )
    examperiod = models.ManyToManyField( 'examperiod', through='concern', related_name='examperiod' )

    def __unicode__( self ):
        return self.name + " - " + self.classlevel.name + " (" + self.school.name + ")"



class concern ( models.Model ):

    class Meta:
        db_table = 'concern'
    exam_date = models.DateField()
    exam = models.ForeignKey( exam, related_name='concern_exam' )
    examperiod = models.ForeignKey( examperiod, related_name='concern_period' )
    classgrade = models.ForeignKey( classgrades, related_name='concern_class' )

    def __unicode__( self ):
        return self.exam_date + " - " + self.examperiod.name + " (" + self.classgrade.name + "," + self.exam.name + ")"



class read ( models.Model ):

    class Meta:
        db_table = 'read'
    read_date = models.DateField()
    exam = models.ForeignKey( exam, related_name='read_exam' )
    user = models.ForeignKey( user, related_name='read_user' )

    def __unicode__( self ):
        return self.user.name + " - " + self.exam.name + " (" + self.read_date + ")"



class submit ( models.Model ):

    class Meta:
        db_table = 'submit'
    submit_date = models.DateField()
    exam = models.ForeignKey( exam, related_name='submit_exam' )
    user = models.ForeignKey( user, related_name='submit_user' )

    def __unicode__( self ):
        return self.user.name + " - " + self.exam.name + " (" + self.submit_date + ")"



class comment ( models.Model ):

    class Meta:
        db_table = 'comment'
    comment_date = models.DateField()
    comment = models.TextField( max_length=30 )
    exam = models.ForeignKey( exam, related_name='comment_exam' )
    user = models.ForeignKey( user, related_name='comment_read' )

    def __unicode__( self ):
        return self.user.name + " - " + self.exam.name + " - " + self.comment + " (" + self.comment_date + ")"



class propose( models.Model ):

    class Meta:
        db_table = 'propose'
    proposition_date = models.DateField()
    correction = models.ForeignKey( correction, related_name='propose_correction' )
    exam = models.ForeignKey( exam, related_name='propose_exam' )
    user = models.ForeignKey( user, related_name='propose_user' )

    def __unicode__( self ):
        return self.user.name + " - " + self.exam.name + self.correction.fields + " (" + self.comment_date + ")"
