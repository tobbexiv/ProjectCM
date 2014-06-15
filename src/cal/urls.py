from django.conf.urls import patterns, url

urlpatterns = patterns('',
        url(r'^$', 'cal.views.calendar_list', name='calendar_list'),
        url(r'^new$', 'cal.views.calendar_create', name='calendar_create'),
        url(r'^view/(?P<pk>\d+)$', 'cal.views.calendar_view', name='calendar_view'),
        url(r'^edit/(?P<pk>\d+)$', 'cal.views.calendar_update', name='calendar_update'),
        url(r'^delete/(?P<pk>\d+)$', 'cal.views.calendar_delete', name='calendar_delete'),
	url(r'^appointment/list$', 'cal.views.appointment_list', name='appointment_view'),
	url(r'^appointment/create$', 'cal.views.appointment_create', name='appointment_create'),
	url(r'^appointment/updte/(P<pk>\+)$', 'cal.views.appointment_update', name='appointment_update'),
	url(r'^appointment/delete/(P<pk>\+)$', 'cal.views.appointment_delete', name='appointment_delete'),


)

