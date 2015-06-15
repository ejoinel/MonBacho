#-*- coding: utf-8 -*-

from django.contrib import admin
from MonBacho.models import exam, concern, user, student, professor, correction, read, propose, classgrades, examperiod, comment, classlevel, school

class useradmin( admin.ModelAdmin ):
    list_display = ( 'firstname', 'mail', 'school' )
    list_filter = ( 'firstname', 'mail', 'school' )
    date_hierarchy = 'creation_date'
    ordering = ( 'creation_date', )
    search_fields = ( 'firstname', 'lastname', 'nickname', 'login' )

admin.site.register( correction )
admin.site.register( read )
admin.site.register( propose )
admin.site.register( classgrades )
admin.site.register( examperiod )
admin.site.register( comment )
admin.site.register( user, useradmin )
admin.site.register( student )
admin.site.register( professor )
admin.site.register( exam )
admin.site.register( concern )
admin.site.register( classlevel )
admin.site.register( school )
