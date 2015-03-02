#-*- coding: utf-8 -*-

from django.contrib import admin
from MonBacho.models import exam, concern, user, student, professor, correction, read, propose, classgrades, examperiod, comment, classlevel, school

admin.site.register(correction)
admin.site.register(read)
admin.site.register(propose)
admin.site.register(classgrades)
admin.site.register(examperiod)
admin.site.register(comment)
admin.site.register(user)
admin.site.register(student)
admin.site.register(professor)
admin.site.register(exam)
admin.site.register(concern)
admin.site.register(classlevel)
admin.site.register(school)
