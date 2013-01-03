#coding=UTF-8

from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
import os

from etask.models import task_list, task

class subnav_button_data:
    def __init__(self):
        self.button_data = [
            [10, 'fulfill', '完成', 'none', 'show'],
            [20, 'move', '移至', 'dropdown', 'show'],
            [30, 'delete', '删除', 'none', 'show'],
        ]
        
    def add_dropdown_menu(self, name, menu):
        for button in self.button_data:
            if name in button:
                button.append(menu)                
        
    def change_state(self, key, state):
        for keys in key:
            if keys in self.button_data:
                self.button_data[keys][3] = state
            
    def change_key(self, key, target_key):
        if key in self.button_data:
            self.button_data[target_key] = self.button_data[key]
            del self.button_data[key]           
            
    def button_sort(self):
        id_sort_list = []
        button_data_sort = []
        
        for ids in self.button_data:
            index = self.button_data.index(ids)
            id_sort_list.append([ids[0],index])
            
        id_sort_list.sort()
        
        for ids in id_sort_list:
            button_data_sort.append(self.button_data[ids[1]])
           
        return button_data_sort
        
def index(request):
    list_id=0
    return HttpResponseRedirect(reverse('etask.views.views_task_list', args=(list_id,)))

def views_task_list(request, list_id):
    list_id = int(list_id)
    latest_task_list = task_list.objects.all().order_by('pub_date')
    url_actions = os.path.join(request.path, 'actions/')
    
    data = subnav_button_data()
    button_data = data.button_sort()
    
    menu = []
    if list_id == 0:
        for task_lists in latest_task_list:
            menu.append(task_lists.list_name)         
            data.add_dropdown_menu('移至', menu)
    else:
        now_list = latest_task_list.get(pk=list_id)
        if (now_list.list_name != '存档') and (now_list.list_name != '回收站'):
            for task_lists in latest_task_list:
                menu.append(task_lists.list_name)         
                data.add_dropdown_menu('移至', menu)
            
    if list_id == 0:
        all_task = task.objects.all().order_by('task_list', '-priority', 'pub_date')
    else:
        t = task_list.objects.get(pk=list_id)  
        all_task = t.task_set.all().order_by('task_list', '-priority', 'pub_date')
    
    c = RequestContext(request, {
        'latest_task_list': latest_task_list,
        'all_task': all_task,
        'etask': 'yes',
        'activeid': list_id,
        'url_actions': url_actions,
        'button_data': button_data,
    })
    
    return render_to_response('etask/index.html', c)

def actions(request, list_id):
    list_id = int(list_id)     
    queryset = querysets(request)
    
    if request.POST.has_key('fulfill'):
        move_task(queryset, '存档')
        return return_http(list_id)   

    elif request.POST.has_key('move'):
        
        return HttpResponse('移动')
        
    elif request.POST.has_key('delete'):
        move_task(queryset, '回收站')
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
    list_id = int(list_id)
    return HttpResponseRedirect(reverse('etask.views.views_task_list', args=(list_id,)))
        
def move_task(queryset, list_names):
    recycle = task_list.objects.get(list_name=list_names)
    queryset.update(task_list=recycle)