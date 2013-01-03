#coding=UTF-8

from etask.models import task_list, task

def all_task_list():
    latest_task_list = task_list.objects.all()
    all_task_list = []
    
    for task_list_obj in  latest_task_list:
        if (task_list_obj.id != 6) and (task_list_obj.id != 7):
            all_task_list.append(task_list_obj.id)
            
    return all_task_list

print all_task_list()



            

