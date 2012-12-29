#coding=UTF-8

from polls.models import Poll, Choice
from django.contrib import admin

class ChoiceInline(admin.TabularInline):

    model = Choice
    extra = 0

class PollAdmin(admin.ModelAdmin):

    fieldsets = [
        (None,      {'fields': ['question']}),
        ('日期信息', {'fields': ['pub_date']}),
        ]

    inlines = [ChoiceInline]
    
    list_display = ('question', 'pub_date', 'choice_num')    
    list_filter = ['pub_date']
    search_fields = ['question']

admin.site.register(Poll, PollAdmin)