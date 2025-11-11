from django.contrib import admin

from django.contrib import admin
from .models import Subject  



admin.site.register(Subject)

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'credits')  
    search_fields = ('name', 'code') 
