#-*- coding: utf-8 -*-

from django.db import models


STUDENT_TYPE_CHOICES = (
    ('0', 'Terminale'),
    ('1', 'Troisième'),
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
    school = models.IntegerField(choices=SCHOOL_TYPE_CHOICES, default=0)
    function = models.CharField(max_length=50)

    def __unicode__(self):
        return self.sex + " " + self.nickname + "(" + self.nickname + ")"




class course (models.Model):

    class Meta:
        db_table = 'course'
    name = models.CharField(max_length=30)
    subject = models.ForeignKey(subject, null=True, blank=True, default=None)

    def __unicode__(self):
        return self.name



class examen (models.Model):

    class Meta:
        db_table = 'examen'
    name = models.CharField(max_length=30)
    is_real_examen = models.BooleanField(default=True)
    subject = models.ManyToManyField('subject', through='concern', related_name='subject')

    def __unicode__(self):
        return self.name + " " + self.is_real_examen



class classgrades (models.Model):

    class Meta:
        db_table = 'classgrade'
    name = models.CharField(max_length=30)
    creation_date = models.DateField()
    school = models.IntegerField(choices=SCHOOL_TYPE_CHOICES, default=0)
    grade = models.IntegerField(choices=STUDENT_TYPE_CHOICES, default=0)
    examen = models.ManyToManyField('examen', through='concern', related_name='examen')

    def __unicode__(self):
        return self.name



class concern (models.Model):

    class Meta:
        db_table = 'concern'
    exam_date = models.DateField()
    subject = models.ForeignKey(subject, related_name='PassExam')
    examen = models.ForeignKey(examen, related_name='PassExam')
    classgrade = models.ForeignKey(classgrades, related_name='PassExam')

    def __unicode__(self):
        return self.pass_date + " - " + self.examen.name + " (" + self.classgrade.name + "," + self.subject.name + ")"


