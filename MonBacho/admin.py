#-*- coding: utf-8 -*-

from django.contrib import admin
from MonBacho.models import Document, Exam, User, Correction, Read, Submit, Comment, ClassLevel, School, ClassTopic

# class useradmin(admin.ModelAdmin):
#      list_display = ('first_name', 'email', 'school')
#      list_filter = ('first_name', 'email', 'school')
#      date_hierarchy = 'date_joined'
#      ordering = ('date_joined',)
#      #search_fields = ('first_name', 'last_name', 'email')

admin.site.register(Document)
admin.site.register(Submit)
admin.site.register(ClassTopic)
admin.site.register(Correction)
admin.site.register(Read)
admin.site.register(Comment)
admin.site.register(User)
#admin.site.register(useradmin)
admin.site.register(Exam)
admin.site.register(ClassLevel)
admin.site.register(School)
