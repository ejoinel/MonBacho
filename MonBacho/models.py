#-*- coding: utf-8 -*-

from django.db import models



class classtypes (models.Model):

    class Meta:
        db_table = 'classtype'
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name



class subjects (models.Model):

    class Meta:
        db_table = 'subject'
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name



class courses (models.Model):

    class Meta:
        db_table = 'course'
    name = models.CharField(max_length=30)
    subject = models.ForeignKey(subjects, null=True, blank=True, default=None)

    def __unicode__(self):
        return self.name



class examens (models.Model):

    class Meta:
        db_table = 'examen'
    name = models.CharField(max_length=30)
    is_real_examen = models.BooleanField(default=True)
    subject = models.ManyToManyField('subjects', through='concern', related_name='subject')

    def __unicode__(self):
        return self.name + " " + self.is_real_examen



class schools (models.Model):

    class Meta:
        db_table = 'school'
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name



class classgrades (models.Model):

    class Meta:
        db_table = 'classgrade'
    name = models.CharField(max_length=30)
    creation_date = models.DateField()
    school = models.ForeignKey(schools, null=True, blank=True, default=None)
    examen = models.ManyToManyField('examens', through='concern', related_name='examens')

    def __unicode__(self):
        return self.name



class concern (models.Model):

    class Meta:
        db_table = 'concern'
    examdate = models.DateField()
    subject = models.ForeignKey(subjects, related_name='PassExam')
    examen = models.ForeignKey(examens, related_name='PassExam')
    classgrade = models.ForeignKey(classgrades, related_name='PassExam')

    def __unicode__(self):
        return self.pass_date + " - " + self.examen.name + " (" + self.classgrade.name + "," + self.subject.name + ")"

