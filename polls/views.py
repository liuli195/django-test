#coding=UTF-8

from django.template import RequestContext
from polls.models import Poll, Choice
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse

def index(request):

    latest_poll_list = Poll.objects.all().order_by('-pub_date')
    c = RequestContext(request, {
        'latest_poll_list': latest_poll_list,
    })

    return render_to_response('polls/index.html', c)

def detail(request, poll_id):
    
    p = get_object_or_404(Poll, pk=poll_id)
    c = RequestContext(request, {
        'poll': p,
        })
    return render_to_response('polls/detail.html', c)

def vote(request, poll_id):

    p = get_object_or_404(Poll, pk=poll_id)

    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render_to_response('polls/detail.html', RequestContext(request, {
            'poll': p,
            'error_message': "你没有选择任何选项，请选择一个选项！",
        }))
    else:
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))

def results(request, poll_id):

    p = get_object_or_404(Poll, pk=poll_id)
    c = RequestContext(request, {
        'poll': p,
        })
    return render_to_response('polls/results.html', c)
