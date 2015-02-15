#-*- coding: utf-8 -*-

from django.contrib import admin
from MonBacho.models import course, examen, concern, subject, personne, student, professor

admin.site.register(course)
admin.site.register(personne)
admin.site.register(student)
admin.site.register(professor)
admin.site.register(subject)
admin.site.register(examen)
admin.site.register(concern)
