#coding=UTF-8

from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
import os

from etask.models import task_list, task

def index_re(request):
    return HttpResponseRedirect(os.path.join(request.path, '0/'))
        
def index(request, list_id, run):
    list_id = int(list_id)
    data = handle_data(request, list_id)
    
    return run(request, data)

def views_task_list(request, data):
    
    c = RequestContext(request, {
        'latest_task_list': data.latest_task_list,
        'all_task': data.all_task,
        'etask': 'yes',
        'activeid': data.list_id,
        'url_actions': data.url_actions,
        'button_data': data.button_data,
        'data': data,
    })
    
    return render_to_response('etask/index.html', c)

def actions(request, data):
    list_id = data.list_id
    admin_actions = admin_action(request, list_id)
    admin_actions.Dispatcher()
    
    return admin_actions.return_http()

class temporary_data:
    def __init__(self, request):
        self.button_data = self.init_data()
        self.button_data = self.button_sort()
        self.url_actions = os.path.join(request.path, 'actions/')
        
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

class handle_data(temporary_data):
    def __init__(self, request, list_ids):
        temporary_data.__init__(self, request)
        self.request = request
        self.latest_task_list = task_list.objects.all().order_by('pub_date')
        self.list_id = list_ids
        self.set_button_data()
        self.set_task_data()
        self.show_message()
          
    def set_button_data(self):
        if self.list_id == 6:
            self.change(['fulfill', 'delete'], 4, 'hide')
            self.change(['redel'], 4, 'show')
        elif self.list_id == 7:
            self.change(['fulfill', 'delete'], 4, 'hide')
            
        self.change(['move'], 5, self.menu_data())
      
    def set_task_data(self):  
        if self.list_id == 0:
            all_task_lists = self.all_task_list()
            self.all_task = task.objects.filter(task_list__in=all_task_lists).order_by('task_list', '-priority', 'pub_date')
        else:
            t = task_list.objects.get(pk=self.list_id)
            self.all_task = t.task_set.all().order_by('task_list', '-priority', 'pub_date')
    
    def menu_data(self):
        
        if self.list_id == 0:
            menu = self.remove_menu()            
        elif self.list_id == 6:
            menu = self.remove_menu([self.list_id, 7])
        elif self.list_id == 7:
            menu = self.remove_menu([self.list_id, 6])                     
        else:
            menu = self.remove_menu([self.list_id]) 
        
        return menu    
    
    def remove_menu(self, id_list=None):
        menu = []
        
        for task_lists in self.latest_task_list:
            if id_list == None:
                menu.append(task_lists)
            else:
                if task_lists.id not in id_list:
                    menu.append(task_lists) 
                        
        return menu
  
    def all_task_list(self):
        all_task_list = []
        
        for task_list_obj in  self.latest_task_list:
            if (task_list_obj.id != 6) and (task_list_obj.id != 7):
                all_task_list.append(task_list_obj.id)
                
        return all_task_list
    
    def show_message(self):
        if 'message' in self.request.session:
            messages = self.request.session['message']
            
            if messages[1] == "show":
                self.message = messages[0]
                
            del self.request.session['message']
    
class admin_action:
    def __init__(self, requests, list_ids):
        self.request = requests
        self.list_id = list_ids
        self.queryset = self.querysets()
    
    def Dispatcher(self):
        
        if self.request.POST.has_key('fulfill'):
            self.move_task('存档')
            
            count = self.queryset.count()
            self.set_message(['已将%s个任务存档！' % count, 'show'])
    
        elif self.request.POST.has_key('move'): 
            target_list_id = self.request.POST.get('move')
            task_list_obj = task_list.objects.get(pk=int(target_list_id))
            task_list_name = task_list_obj.list_name
            self.move_task(task_list_name)
            
            count = self.queryset.count()
            self.set_message(['已将%s个任务移至%s' % (count, str(task_list_name)), 'show'])
            
        elif self.request.POST.has_key('delete'):
            self.move_task('回收站')
        
        elif self.request.POST.has_key('redel'):
            self.queryset.delete()
        
        elif self.request.POST.has_key('add'):
            
            return HttpResponse('新增')
    
    def querysets(self):
        value_list=[]
        
        for key in self.request.POST: 
            if str(key).find('chioce') != -1:     
                value_list.append(self.request.POST.get(key))
                
        return task.objects.filter(pk__in=value_list)
    
    def return_http(self):
        return HttpResponseRedirect(os.path.dirname(os.path.dirname(self.request.path)))
            
    def move_task(self, list_names):
        recycle = task_list.objects.get(list_name=list_names)
        self.queryset.update(task_list=recycle)
        
    def set_message(self, message):
        self.request.session['message'] = message

        