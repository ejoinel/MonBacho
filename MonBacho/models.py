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



class subject (models.Model):

    class Meta:
        db_table = 'subject'
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name



class personne(models.Model):

    class Meta:
        db_table = 'person'

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



class student(personne):

    class Meta:
        db_table = 'student'

    grade = models.IntegerField(choices=STUDENT_TYPE_CHOICES, default=0)

    def __unicode__(self):
        return self.nickname + "(" + self.nickname + ")"



class professor(personne):

    class Meta:
        db_table = 'professor'

    school = models.IntegerField(choices=SCHOOL_TYPE_CHOICES, default=0)
    function = models.CharField(max_length=50)

    def __unicode__(self):
        return self.sex + " " + self.nickname + "(" + self.nickname + ")"



class exam (models.Model):

    class Meta:
        db_table = 'exam'
    name = models.CharField(max_length=30)
    creation_date = models.DateField()
    matter = models.IntegerField(choices=MATTER_TYPE_CHOICES, default=0)
    creator = models.ForeignKey(personne)

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
        return self.pass_date + " - " + self.examen.name + " (" + self.classgrade.name + "," + self.subject.name + ")"


