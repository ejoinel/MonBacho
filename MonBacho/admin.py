#-*- coding: utf-8 -*-

from django.contrib import admin
from MonBacho.models import classtypes, schools, classgrades, subjects, courses, examens, concern

admin.site.register(schools)
admin.site.register(classgrades)
admin.site.register(classtypes)
admin.site.register(courses)
admin.site.register(subjects)
admin.site.register(examens)
admin.site.register(concern)
