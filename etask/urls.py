from django.conf.urls import patterns, url

urlpatterns = patterns('etask.views',
    url(r'^$', 'index'),
    url(r'^(?P<list_id>\d+)/$', 'views_task_list'),
    url(r'^(?P<list_id>\d+)/actions/$', 'actions'),
    #url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)
