#-*- coding: utf-8 -*-

from django.db import models


STUDENT_TYPE_CHOICES = (
    ('0', 'Terminale'),
    ('1', 'Troisième'),
)



MATTER_TYPE_CHOICES = (
    ('0', 'Mathématique'),
    ('1', 'Français'),
    ('2', 'SVT'),
    ('3', 'Musique'),
    ('4', 'Anglais'),
    ('5', 'Philosophie'),
    ('6', 'Espagnol'),
    ('7', 'Physique-Chimie')
)



PERSON_SEX_CHOISE = (
    ('0', 'Mr'),
    ('1', 'Mme'),
    ('2', 'Mlle')
)



SCHOOL_TYPE_CHOICES = (
    ('0', 'Lycée Leon MBA'),
    ('1', 'Collège Béssieux'),
)



class user(models.Model):

    class Meta:
        db_table = 'user'

    sex = models.IntegerField(choices=PERSON_SEX_CHOISE, default=0)
    name = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30)
    birth_date = models.DateField()
    mail = models.EmailField()
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=32)

    def __unicode__(self):
        return self.nickname + "(" + self.nickname + ")"



class student(user):

    class Meta:
        db_table = 'student'

    grade = models.IntegerField(choices=STUDENT_TYPE_CHOICES, default=0)

    def __unicode__(self):
        return self.nickname + "(" + self.nickname + ")"



class professor(user):

    class Meta:
        db_table = 'professor'

    school = models.IntegerField(choices=SCHOOL_TYPE_CHOICES, default=0)
    function = models.CharField(max_length=50)

    def __unicode__(self):
        return self.sex + " " + self.nickname + "(" + self.nickname + ")"



class correction(user):

    class Meta:
        db_table = 'correction'

    creation_date = models.DateField()
    fields = models.CharField(max_length=50)

    def __unicode__(self):
        return self.fields + " " + self.creation_date



class exam (models.Model):

    class Meta:
        db_table = 'exam'
    name = models.CharField(max_length=30)
    creation_date = models.DateField()
    matter = models.IntegerField(choices=MATTER_TYPE_CHOICES, default=0)
    creator = models.ForeignKey(user)
    corrections = models.ManyToManyField('correction', through='propose', related_name='correction')

    def __unicode__(self):
        return self.name + " " + self.matter



class examperiod (models.Model):

    class Meta:
        db_table = 'examperiod'
    name = models.CharField(max_length=30)
    mock_exam = models.BooleanField(default=True)
    examens = models.ManyToManyField('exam', through='concern', related_name='exam')

    def __unicode__(self):
        return self.name + " " + self.is_real_examen



class classgrades (models.Model):

    class Meta:
        db_table = 'classgrade'
    name = models.CharField(max_length=30)
    creation_date = models.DateField()
    school = models.IntegerField(choices=SCHOOL_TYPE_CHOICES, default=0)
    grade = models.IntegerField(choices=STUDENT_TYPE_CHOICES, default=0)
    examperiod = models.ManyToManyField('examperiod', through='concern', related_name='examperiod')

    def __unicode__(self):
        return self.name



class concern (models.Model):

    class Meta:
        db_table = 'concern'
    exam_date = models.DateField()
    exam = models.ForeignKey(exam, related_name='concern_exam')
    examperiod = models.ForeignKey(examperiod, related_name='concern_period')
    classgrade = models.ForeignKey(classgrades, related_name='concern_class')

    def __unicode__(self):
        return self.exam_date + " - " + self.examperiod.name + " (" + self.classgrade.name + "," + self.exam.name + ")"



class read (models.Model):

    class Meta:
        db_table = 'read'
    read_date = models.DateField()
    exam = models.ForeignKey(exam, related_name='read_exam')
    user = models.ForeignKey(user, related_name='read_user')

    def __unicode__(self):
        return self.user.name + " - " + self.exam.name + " (" + self.read_date + ")"



class comment (models.Model):

    class Meta:
        db_table = 'comment'
    comment_date = models.DateField()
    comment = models.TextField(max_length=30)
    exam = models.ForeignKey(exam, related_name='comment_exam')
    user = models.ForeignKey(user, related_name='comment_read')

    def __unicode__(self):
        return self.user.name + " - " + self.exam.name + " - " + self.comment + " (" + self.comment_date + ")"



class propose(models.Model):

    class Meta:
        db_table = 'propose'
    proposition_date = models.DateField()
    correction = models.ForeignKey(correction, related_name='propose_correction')
    exam = models.ForeignKey(exam, related_name='propose_exam')
    user = models.ForeignKey(user, related_name='propose_user')

    def __unicode__(self):
        return self.user.name + " - " + self.exam.name + self.correction.fields + " (" + self.comment_date + ")"
