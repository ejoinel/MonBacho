#-*- coding: utf-8 -*-

from django.contrib import admin
from MonBacho.models import Document, Exam, User, Correction, Read, Submit, Comment, ClassLevel, School, ClassTopic

class useradmin( admin.ModelAdmin ):
    list_display = ( 'firstname', 'mail', 'school' )
    list_filter = ( 'firstname', 'mail', 'school' )
    date_hierarchy = 'creation_date'
    ordering = ( 'creation_date', )
    search_fields = ( 'firstname', 'lastname', 'nickname', 'login' )

admin.site.register( Document )
admin.site.register( Submit )
admin.site.register( ClassTopic )
admin.site.register( Correction )
admin.site.register( Read )
admin.site.register( Comment )
admin.site.register( User, useradmin )
admin.site.register( Exam )
admin.site.register( ClassLevel )
admin.site.register( School )

