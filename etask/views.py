#coding=UTF-8

from django.template import Context, RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
import os

from etask.models import task_list, task

def index(request):

    latest_task_list = task_list.objects.all().order_by('pub_date')
    all_task = task.objects.all().order_by('task_list', '-priority', 'pub_date')
    url_actions = os.path.join(request.path, 'actions')
    
    c = RequestContext(request, {
        'latest_task_list': latest_task_list,
        'all_task': all_task,
        'etask': 'yes',
        'appname': 'Easy Task',
        'note': '轻量级的任务管理系统',
        'activeid': 'home',
        'url_actions': url_actions,
    })

    return render_to_response('etask/index.html', c)

def t_list(request, list_id):
    
    latest_task_list = task_list.objects.all().order_by('pub_date')
    t = task_list.objects.get(pk=list_id)
    all_task = t.task_set.all().order_by('task_list', '-priority', 'pub_date')
    url_actions = os.path.join(request.path, 'actions')
    
    c = RequestContext(request, {
        'latest_task_list': latest_task_list,
        'all_task': all_task,
        'etask': 'yes',
        'appname': 'Easy Task',
        'note': '轻量级的任务管理系统',
        'activeid': t.id,
        'url_actions': url_actions,
    })
    
    return render_to_response('etask/index.html', c)

def actions(request):
    
    if request.POST.has_key('fulfill'):
        
        print 1
        
    elif request.POST.has_key('move'):
        
        print 2
        
    elif request.POST.has_key('delete'):
        
        print 3
        
    
    
    
    