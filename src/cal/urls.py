from django.conf.urls import patterns, url

urlpatterns = patterns('',
        url(r'^$', 'cal.views.calendar_list', name='calendar_list'),
        url(r'^new$', 'cal.views.calendar_create', name='calendar_create'),
        url(r'^view/(?P<pk>\d+)$', 'cal.views.calendar_view', name='calendar_view'),
        url(r'^edit/(?P<pk>\d+)$', 'cal.views.calendar_update', name='calendar_update'),
        url(r'^delete/(?P<pk>\d+)$', 'cal.views.calendar_delete', name='calendar_delete'),
)

