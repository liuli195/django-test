#coding=UTF-8

from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
import os

from etask.models import task_list, task

class subnav_button_data:
    def __init__(self):
        self.button_data = self.init_data()
        self.button_data = self.button_sort()
        
    def init_data(self):
        self.init_button_data = [
            [10, 'fulfill', '完成', 'none', 'show', []],
            [20, 'move', '移至', 'dropdown', 'show', []],
            [30, 'delete', '删除', 'none', 'show', []],
            [15, 'redel', '彻底删除', 'none', 'hide', []],
        ]
        
        return self.init_button_data
        
    def change(self, names, index, value):
        for button in self.button_data:
            for name in names:
                if name in button:
                    button[index] = value    
            
    def button_sort(self):
        id_sort_list = []
        button_data_sort = []
        
        for button in self.button_data:
            index = self.button_data.index(button)
            id_sort_list.append([button[0],index])
            
        id_sort_list.sort()
        
        for ids in id_sort_list:
            button_data_sort.append(self.button_data[ids[1]])
           
        return button_data_sort
        
def index(request):
    list_id = 0
    return HttpResponseRedirect(reverse('etask.views.views_task_list', args=(list_id,)))

def views_task_list(request, list_id):
    admin = admin_views_task_list()
  
    list_id = int(list_id)
    url_actions = os.path.join(request.path, 'actions/')
    
    c = RequestContext(request, {
        'latest_task_list': admin.latest_task_list,
        'all_task': admin.set_task_data(list_id),
        'etask': 'yes',
        'activeid': list_id,
        'url_actions': url_actions,
        'button_data': admin.set_button_data(list_id),
    })
    
    return render_to_response('etask/index.html', c)

class admin_views_task_list:
    def __init__(self):
        self.data = subnav_button_data()
        self.latest_task_list = task_list.objects.all().order_by('pub_date')
          
    def set_button_data(self, list_id):
        if list_id == 6:
            self.data.change(['fulfill', 'delete'], 4, 'hide')
            self.data.change(['redel'], 4, 'show')
        elif list_id == 7:
            self.data.change(['fulfill', 'delete'], 4, 'hide')
            
        self.data.change(['move'], 5, self.menu_data(list_id))
        
        return self.data.button_data
      
    def set_task_data(self, list_id):       
        if list_id == 0:
            all_task_lists = self.all_task_list()
            all_task = task.objects.filter(task_list__in=all_task_lists).order_by('task_list', '-priority', 'pub_date')
        else:
            t = task_list.objects.get(pk=list_id)
            all_task = t.task_set.all().order_by('task_list', '-priority', 'pub_date')
        
        return all_task 
    
    def menu_data(self, list_id):
        
        if list_id == 0:
            menu = self.remove_menu()            
        elif list_id == 6:
            menu = self.remove_menu([list_id, 7])
        elif list_id == 7:
            menu = self.remove_menu([list_id, 6])                     
        else:
            menu = self.remove_menu([list_id]) 
        
        return menu    
    
    def remove_menu(self, id_list=None):
        menu = []
        marks = 0
        
        for task_lists in self.latest_task_list:
            if id_list == None:
                menu.append(task_lists)
            else:
                for list_id in id_list:
                    if task_lists.id == list_id:
                        marks = 1
                        
                if marks != 1:      
                    menu.append(task_lists) 
        return menu
  
    def all_task_list(self):
        all_task_list = []
        
        for task_list_obj in  self.latest_task_list:
            if (task_list_obj.id != 6) and (task_list_obj.id != 7):
                all_task_list.append(task_list_obj.id)
                
        return all_task_list

def actions(request, list_id):
    list_id = int(list_id)     
    queryset = querysets(request)
    
    if request.POST.has_key('fulfill'):
        move_task(queryset, '存档')
        return return_http(list_id)   

    elif request.POST.has_key('move'):       
        target_list_id = request.POST.get('move')
        task_list_obj = task_list.objects.get(pk=int(target_list_id))
        task_list_name = task_list_obj.list_name
        move_task(queryset, task_list_name)
        return return_http(list_id)
        
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