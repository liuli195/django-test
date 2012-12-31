#coding=UTF-8

from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    
    c = RequestContext(request, {
        'home': 'yes',
        'appname': 'Home Page',
        'note': '导航到应用和管理后台',
    })

    return render_to_response('home/index.html', c)
