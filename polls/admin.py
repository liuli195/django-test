#coding=UTF-8

from polls.models import Poll, Choice
from django.contrib import admin
from django.template.response import TemplateResponse
from django.contrib.admin.util import model_ngettext
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _

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
    '''
    actions = ['make_published']
    
    def make_published(self, request, queryset):
        rows_updated = queryset.update(question='p')
        if rows_updated == 1:
            message_bit = "1 story was"
        else:
            message_bit = "%s stories were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)
         
    make_published.short_description = "Mark selected"
    '''
class ChoiceAdmin(admin.ModelAdmin):
    
    list_display = ('poll', 'choice', 'votes')    
    list_filter = ['poll']
    search_fields = ['choice']
    
    actions = ['export_selected_objects']

    def export_selected_objects(self, request, queryset):
        
        opts = self.model._meta
        app_label = opts.app_label
        polls_list = Poll.objects.all()
        
        context = {
        'title': '修改问题',
        'queryset': queryset,
        "opts": opts,
        "app_label": app_label,
        "polls_list":  polls_list
        }
        
        if request.POST.get('post'):

            n = queryset.count()
            if n:
                for obj in queryset:
                    obj_display = force_unicode(obj)
                    self.log_change(request, obj, obj_display)
                    queryset.all().update(votes=int(request.POST['poll']))
                    self.message_user(request, _("成功修改 %(count)个 %(items)。") % {
                        "count": n, "items": model_ngettext(self.opts, n)
                    })

            #return None
            
            #return TemplateResponse(request, 'admin/test.html', {
                    #"opts": opts,
                    #"app_label": app_label,
                    #"choices": request.POST['choice'],
                #})

        return TemplateResponse(request, 'admin/test.html', context)
    
    export_selected_objects.short_description = '修改'

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice, ChoiceAdmin)