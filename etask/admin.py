#coding=UTF-8

from etask.models import task_list, task
from django.contrib import admin

class taskinline(admin.TabularInline):

    model = task
    extra = 0

class task_list_admin(admin.ModelAdmin):

    fieldsets = [
        ('基本信息', {'fields': ['list_name']}),
        ('时间信息', {'fields': ['pub_date']}),
        ]

    inlines = [taskinline]
    
    list_display = ('list_name', 'pub_date', 'task_num')    
    list_filter = ['pub_date']
    search_fields = ['list_name']
    
class taskadmin(admin.ModelAdmin):
    
    fieldsets = [
        ('基本信息', {'fields': ['task_list', 'task_text', 'priority']}),
        ('时间信息', {'fields': ['pub_date']}),
        ]
    
    list_display = ('task_text', 'task_list', 'priority', 'pub_date')    
    list_filter = ['task_list', 'pub_date']
    search_fields = ['task_text']

admin.site.register(task_list, task_list_admin)
admin.site.register(task, taskadmin)