#coding=UTF-8

from django.db import models

class Poll(models.Model):
    
    question = models.CharField('问题', max_length=200)
    pub_date = models.DateTimeField('创建日期')
    
    class Meta:
        verbose_name = '投票'
        verbose_name_plural = '投票列表'
        
    def __unicode__(self):
        return self.question
    
    def choice_num(self):
        return self.choice_set.count()
    
    choice_num.short_description = '选项数量'
    
class Choice(models.Model):
    
    poll = models.ForeignKey(Poll)
    choice = models.CharField('选项', max_length=200)
    votes = models.IntegerField('票数')
    
    class Meta:
        verbose_name = '选项'
        verbose_name_plural = '选项信息'
    
    def __unicode__(self):
        return self.choice