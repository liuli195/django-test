from django.conf.urls import patterns, url
from etask import views

urlpatterns = patterns('etask.views',
    url(r'^$', 'index_re'),
    url(r'^(?P<list_id>\d+)/$', 'index', {'run': views.views_task_list}),
    url(r'^(?P<list_id>\d+)/actions/$', 'index', {'run': views.actions}),
    #url(r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)
