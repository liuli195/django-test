#coding=UTF-8

from django.template import Context, RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

from etask.models import task_list, task

def index(request):

    latest_task_list = task_list.objects.all().order_by('-pub_date')
    c = RequestContext(request, {
        'latest_task_list': latest_task_list,
    })

    return render_to_response('etask/index.html', c)


