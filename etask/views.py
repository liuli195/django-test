#coding=UTF-8

from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
import os

from etask.models import task_list, task

def index(request):

    latest_task_list = task_list.objects.all().order_by('pub_date')
    all_task = task.objects.all().order_by('task_list', '-priority', 'pub_date')
    url_actions = os.path.join(request.path, 'actions/')
    
    c = RequestContext(request, {
        'latest_task_list': latest_task_list,
        'all_task': all_task,
        'etask': 'yes',
        'activeid': 'home',
        'url_actions': url_actions,
    })

    return render_to_response('etask/index.html', c)

def t_list(request, list_id):
    
    latest_task_list = task_list.objects.all().order_by('pub_date')
    t = task_list.objects.get(pk=list_id)
    all_task = t.task_set.all().order_by('task_list', '-priority', 'pub_date')
    url_actions = os.path.join(request.path, 'actions/')
    
    c = RequestContext(request, {
        'latest_task_list': latest_task_list,
        'all_task': all_task,
        'etask': 'yes',
        'activeid': t.id,
        'url_actions': url_actions,
    })
    
    return render_to_response('etask/index.html', c)

def actions(request, list_id=None):   
    
    queryset = querysets(request)
    
    if request.POST.has_key('fulfill'):

        recycle = task_list.objects.get(list_name='存档')
        queryset.update(task_list=recycle)
        '''
        value_list=[]
        
        for key in request.POST: 
        
            if str(key).find('chioce') != -1:      
                value_list.append(request.POST.get(key))
                
        
        queryset = task.objects.filter(pk__in=value_list)
        
        c = RequestContext(request, {
        'queryset': queryset,
        'value_list': value_list,
        'etask': 'yes',
        })
        '''
        return return_http(list_id)
        
        #return render_to_response('etask/test.html', c)

    elif request.POST.has_key('move'):
        
        return HttpResponse('移动')
        
    elif request.POST.has_key('delete'):

        recycle = task_list.objects.get(list_name='回收站')
        queryset.update(task_list=recycle)

        return return_http(list_id)
   
    elif request.POST.has_key('add'):
        
        return HttpResponse('新增')
    
def querysets(request):
    
    value_list=[]
    
    for key in request.POST: 

        if str(key).find('chioce') != -1:      
            value_list.append(request.POST.get(key))
            
    return task.objects.filter(pk__in=value_list)

def return_http(list_id):
           
        if list_id == None:
            return HttpResponseRedirect(reverse('etask.views.index'))
        else:
            return HttpResponseRedirect(reverse('etask.views.t_list', args=(list_id,)))
    