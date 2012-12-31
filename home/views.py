#coding=UTF-8

from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    
    c = RequestContext(request, {
    })

    return render_to_response('home/index.html', c)
