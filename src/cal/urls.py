from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'cal.views.calendar_base', name='calendar_base'),
	url(r'^list/?$', 'cal.views.calendar_list', name='calendar_list'),
	url(r'^new/?$', 'cal.views.calendar_create', name='calendar_create'),
	url(r'^view/(?P<pk>\d+)$', 'cal.views.calendar_view', name='calendar_view'),
	url(r'^edit/(?P<pk>\d+)$', 'cal.views.calendar_update', name='calendar_update'),
	url(r'^delete/(?P<pk>\d+)$', 'cal.views.calendar_delete', name='calendar_delete'),
	url(r'^appointment/list/?$', 'cal.views.appointment_list', name='appointment_view'),
	url(r'^appointment/create/?$', 'cal.views.appointment_create', name='appointment_create'),
	url(r'^appointment/view/(?P<pk>\d+)$', 'cal.views.appointment_view', name='appointment_view'),
	url(r'^appointment/update/(?P<pk>\d+)$', 'cal.views.appointment_update', name='appointment_update'),
	url(r'^appointment/delete/(?P<pk>\d+)$', 'cal.views.appointment_delete', name='appointment_delete'),
	url(r'^series/create/?$', 'cal.views.series_create', name='series_create'),
	url(r'^series/delete/(?P<pk>\d+)$', 'cal.views.series_delete', name='series_delete'),
	url(r'^series/view/(?P<pk>\d+)$', 'cal.views.series_view', name='series_view'),
	url(r'^series/update/(?P<pk>\d+)$', 'cal.views.series_update', name='series_update'),
	url(r'^calshare/create/(?P<pk>\d+)?$', 'cal.views.calshare_create', name='calshare_create'),
	url(r'^calshare/list/(?P<pk>\d+)?$', 'cal.views.calshare_list', name='calshare_list'),
	url(r'^calshare/delete/(?P<pk>\d+)$', 'cal.views.calshare_delete', name='calshare_delete'),
)