from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.utils import simplejson
from cal.models import Calendar, Appointment
from cal.forms import CalendarForm
from django.http import HttpResponse
from cal.serializer import CalSerializer
from django.core.serializers.json import DjangoJSONEncoder 
from datetime import datetime, timedelta

@login_required
def calendar_list(request, template_name='calendar/calendar_list.html'):
	ser = CalSerializer()
	calendar = Calendar.objects.filter(calendar_owner=request.user)
	response = {}
	response['userName'] = request.user.username
	response['success'] = True
	response['data'] = ser.serialize(calendar)

	json_response = simplejson.dumps(response)
	return HttpResponse(json_response, content_type="application/json")

@login_required
def calendar_view(request, template_name='calendar/calendar_view.html'):
	calendar = get_object_or_404(Calendar, pk=pk)
	
	return render(request, template_name, {'calendar':calendar})


@login_required
def calendar_create(request):
	form = CalendarForm(request.POST or None)
	if form.is_valid() and request.method == "POST" and request.is_ajax:
		calendar = form.save(commit=False)
		calendar.calendar_owner = request.user
		calendar.save()

		return HttpResponse("data saved")

	return render(request, 'calendar/calendar_form.html', {'form':form})
	


@login_required
def calendar_update(request, pk, template_name='calendar/calendar_form.html'):
        calendar = get_object_or_404(Calendar, pk=pk)
        form = CalendarForm(request.POST or None, instance=calendar)
        if form.is_valid() and request.method == "POST" and request.is_ajax:
                form.save()
                return HttpResponse("data saved")

        return render(request, template_name, {'form':form})

@login_required
def calendar_delete(request, pk, template_name='calendar/calendar_delete.html'):
        calendar = get_object_or_404(Calendar, pk=pk)
        if request.method=='POST' and request.is_ajax:
                calendar.delete()
                return HttpResponse("data deleted")

        return render(request, template_name, {'object':calendar})


@login_required
def appointment_list(request):
	if request.method == "GET": #request.method == "POST" and request.is_ajax:
		json_data = simplejson.loads(request.raw_post_data)
		from_date = json_data['fetch_after_date']
		to_date = json_data['fetch_before_date']
		calendar = json_data['calendar']
		
		ser = CalSerializer()
		all_appointments = []

		appointments = Appointment.objects.filter(calendar=calendar, series=None, start_date__lte=to_date, end_date__gte=from_date)
		all_appointments.append(list(appointments))		


		series = Series.objects.filter(first_occurence__lte=to_date, last_occurence__gte=to_date)
		
		for occ in series:
			ser_apps = Appointment.objects.get(series=occ)
			all_appointments.append(list(ser_apps))
			day1 = (from_date - timedelta(days=from_date.weekday()))
			day2 = (to_date - timedelta(days=to_date.weekday()))

			if occ.reoccurences == 'daily':
				days_between = (days2 - days1).days()

				for i in range(1, days_between):
					new_start_date = ser_apps.start_date + datetime.timedelta(days=1*i)
					new_end_date = ser_apps.end_date + datetime.timedelta(days=1*i)
					all_appointments.append(Appointment(calendar=calendar, title=ser_apps.title, description=ser_apps.description, start_date=new_start_date, end_date=new_end_date))
	
			elif occ.reoccurences == 'weekly':
				weeks_between = (day2 - day1).days() / 7
				
				for i in range(1, weeks_between):
					new_start_date = ser_apps.start_date + datetime.timedelta(days=7*i) 
					new_end_date = ser_apps.end_date + datetime.timedelta(days=7*i)
					all_appointments.append(Appointment(calendar=calendar, title=ser_apps.title, description=ser_apps.description, start_date=new_start_date, end_date=new_end_date))

				
			elif occ.reoccurences == 'monthly':
				pass
			



		response = {}
		response['userName'] = request.user.username
		response['success'] = True
		response['data'] = ser.serialize(appointments)

		json_response = simplejson.dumps(response, cls=DjangoJSONEncoder)
		return HttpResponse(json_response, content_type="application/json")

	else:
		return HttpResponse("invalid request")

		
