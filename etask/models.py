#coding=UTF-8

from django.db import models

class task_list(models.Model):
    
    list_name = models.CharField('名称', max_length=200)
    pub_date = models.DateTimeField('创建时间')
    
    class Meta:
        verbose_name = '任务列表'
        verbose_name_plural = '全部列表'
        
    def __unicode__(self):
        return self.list_name
    
    def task_num(self):
        return self.task_set.count()
    
    task_num.short_description = '任务数量'
    
class task(models.Model):
    
    task_list = models.ForeignKey(task_list, verbose_name='任务列表')
    task_text = models.CharField('任务', max_length=200)
    priority = models.IntegerField('优先级')
    pub_date = models.DateTimeField('创建时间')
    
    class Meta:
        verbose_name = '任务'
        verbose_name_plural = '全部任务'
    
    def __unicode__(self):
        return self.task_text