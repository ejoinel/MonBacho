#-*- coding: utf-8 -*-

from django.contrib import admin
from MonBacho.models import document, exam, user, correction, read, submit, comment, classlevel, school, classtopic

class useradmin( admin.ModelAdmin ):
    list_display = ( 'firstname', 'mail', 'school' )
    list_filter = ( 'firstname', 'mail', 'school' )
    date_hierarchy = 'creation_date'
    ordering = ( 'creation_date', )
    search_fields = ( 'firstname', 'lastname', 'nickname', 'login' )

admin.site.register( document )
admin.site.register( submit )
admin.site.register( classtopic )
admin.site.register( correction )
admin.site.register( read )
admin.site.register( comment )
admin.site.register( user, useradmin )
admin.site.register( exam )
admin.site.register( classlevel )
admin.site.register( school )
