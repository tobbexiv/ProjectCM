from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
import json
from cal.models import Calendar, Appointment, Series, CalendarShare
from cal.forms import CalendarForm, AppointmentForm, SeriesForm, CalShareForm
from django.http import HttpResponse
from cal.serializer import CalSerializer, DateTimeEncoder
from django.core.serializers.json import DjangoJSONEncoder 
from datetime import datetime, timedelta
from django.utils.timezone import utc
import dateutil.parser as dateparser

from django.forms.models import model_to_dict

@login_required
def calendar_base(request, template_name='cal/calendar_base.html'):
	return render(request, template_name, {})

@login_required
def calendar_list(request, template_name='cal/calendar_list.html'):
	ser = CalSerializer()
	calendar = Calendar.objects.filter(calendar_owner=request.user)
	response = {}
	response['userName'] = request.user.username
	response['success'] = True
	response['data'] = ser.serialize(calendar)

	json_response = json.dumps(response)
	return HttpResponse(json_response, content_type="application/json")

@login_required
def calendar_view(request, pk, template_name='cal/calendar_view.html'):
	calendar = get_object_or_404(Calendar, pk=pk)
	
	return render(request, template_name, {'calendar':calendar})


@login_required
def calendar_create(request):
	form = CalendarForm(request.POST or None)
	max_calendars = request.user.profile.max_no_mail_accounts

	if form.is_valid() and request.method == "POST" and request.is_ajax:
		calendar = form.save(commit=False)
		calendar.calendar_owner = request.user
		calendar.save()

		response = {}
		response['userName'] = request.user.username
		response['success'] = True
		response['data'] = 'Calendar successfully created'

		json_response = json.dumps(response)
		return HttpResponse(json_response, content_type="application/json")

	return render(request, 'cal/generic_form.html', {'form':form})
	


@login_required
def calendar_update(request, pk, template_name='cal/generic_form.html'):
		calendar = get_object_or_404(Calendar, pk=pk)
		form = CalendarForm(request.POST or None, instance=calendar)
		if form.is_valid() and request.method == "POST" and request.is_ajax:
				form.save()
				response = {}
				response['userName'] = request.user.username
				response['success'] = True
				response['data'] = 'Calendar successfully updated'

				json_response = json.dumps(response)
				return HttpResponse(json_response, content_type="application/json")

		return render(request, template_name, {'form':form})

@login_required
def calendar_delete(request, pk, template_name='cal/calendar_delete.html'):
		calendar = get_object_or_404(Calendar, pk=pk)
		if request.method=='POST' and request.is_ajax:
				calendar.delete()
				response = {}
				response['userName'] = request.user.username
				response['success'] = True
				response['data'] = 'Calendar successfully deleted'

				json_response = json.dumps(response)
				return HttpResponse(json_response, content_type="application/json")

		return render(request, template_name, {'object':calendar})


@login_required
def appointment_list(request):
	if request.method == "POST" and request.is_ajax: #"GET": 
		json_data = json.loads(request.body.decode('utf-8'))
		# now = datetime.utcnow().replace(tzinfo=utc)
		from_date = dateparser.parse(json_data['fetch_after_date'])
		to_date = dateparser.parse(json_data['fetch_before_date'])

		# from_date = now - timedelta(days=1)
		# to_date = now + timedelta(days=1)

		calendar_list = Calendar.objects.filter(calendar_owner=request.user) 
		
		ser = CalSerializer()
		all_appointments = []

		for calendar in calendar_list:
			appointments = Appointment.objects.filter(calendar=calendar, start_date__lte=to_date, end_date__gte=from_date, series=None) 

			for appo in appointments:						
				all_appointments.append(json.dumps(appo, cls=DateTimeEncoder))  
				
			series = Appointment.objects.filter(calendar=calendar, start_date__lte=to_date, end_date__gte=from_date, series__first_occurence__lte=to_date, series__last_occurence__gte=from_date)	
			
			for appo in series:					
					all_appointments.append(json.dumps(appo, cls=DateTimeEncoder))				

					if appo.series.reoccurences == 'daily':

						
						if appo.series.first_occurence > datetime.date(from_date):
							new_from_date = appo.series.first_occurence
						else:
							new_from_date = datetime.date(from_date)

						if appo.series.last_occurence < datetime.date(to_date):
							new_to_date = appo.series.last_occurence
						else: 	
							new_to_date = datetime.date(to_date)

						days_between = int((new_to_date - new_from_date).days)

														
						for i in range(1, days_between+1):
							new_start_date = appo.start_date + timedelta(days=1*i)
							new_end_date = appo.end_date + timedelta(days=1*i)
							new_app = Appointment(calendar=calendar, title=appo.title, description=appo.description, start_date=new_start_date, end_date=new_end_date)
							
							all_appointments.append(json.dumps(new_app, cls=DateTimeEncoder))
			
					elif appo.series.reoccurences == 'weekly':				

						if appo.series.first_occurence > datetime.date(from_date):
							new_from_date = appo.series.first_occurence
						else:
							new_from_date = datetime.date(from_date)

						if appo.series.last_occurence < datetime.date(to_date):
							new_to_date = appo.series.last_occurence
						else: 	
							new_to_date = datetime.date(to_date)		

						weeks_between = int((new_to_date - new_from_date).days / 7)
					
						for i in range(1, weeks_between+1):
							new_start_date = appo.start_date + timedelta(days=7*i) 
							new_end_date = appo.end_date + timedelta(days=7*i)
							new_app = Appointment(calendar=calendar, title=appo.title, description=appo.description, start_date=new_start_date, end_date=new_end_date)

							all_appointments.append(json.dumps(new_app, cls=DateTimeEncoder))
							
						
					elif appo.series.reoccurences == 'monthly':
						pass        



		response = {}
		response['userName'] = request.user.username
		response['success'] = True
		response['data'] = all_appointments

		json_response = json.dumps(response, cls=DjangoJSONEncoder)
		return HttpResponse(json_response, content_type="application/json")

	else:
		return HttpResponse("invalid request")

@login_required
def appointment_create(request):
	form = AppointmentForm(request.POST or None)
	if form.is_valid() and request.method == "POST" and request.is_ajax:
		appointment = form.save()

		response = {}
		response['userName'] = request.user.username
		response['success'] = True
		response['data'] = 'Appointment successfully created'

		json_response = json.dumps(response)
		return HttpResponse(json_response, content_type="application/json")

	return render(request, 'cal/appointment_form.html')

@login_required
def appointment_update(request, pk, template_name='cal/generic_form.html'):
	appointment = get_object_or_404(Appointment, pk=pk)
	form = AppointmentForm(rquest.POST or None, instance=appointment)
	if form.is_valid() and request.method == "POST" and request.is_ajax:
		form.save()
		response = {}
		response['userName'] = request.user.username
		response['success'] = True
		response['data'] = 'Appointment successfully updated'

		json_response = json.dumps(response)
		return HttpResponse(json_response, content_type="application/json")

	return render(request, template_name, {'form':form})
	

@login_required
def appointment_delete(request, pk, template_name='appointment_delete'):
	appointment = get_object_or_404(Appointment, pk=pk)
	if request.method == "POST" and request.is_ajax:
		appointment.delete()
		response = {}
		response['userName'] = request.user.username
		response['success'] = True
		response['data'] = 'Appointment successfully deleted'

		json_response = json.dumps(response)
		return HttpResponse(json_response, content_type="application/json")

	return render(request, template_name, {'object':appointment})   

@login_required
def series_create(request, template_name='cal/series_create.html'):
	appointment_form = AppointmentForm(request.POST or None)
	series_form = SeriesForm(request.POST or None)

	if appointment_form.is_valid() and series_form.is_valid():
		series = series_form.save()
		appointment = appointment_form.save(commit=False)
		appointment.series = series
		appointment.save()

		response = {}
		response['userName'] = request.user.username
		response['success'] = True
		response['data'] = 'Series successfully created'

		json_response = json.dumps(response)
		return HttpResponse(json_response, content_type="application/json")
		

	data = {}
	data['appointment'] = appointment_form
	data['series'] = series_form

	return render(request, template_name, data)

@login_required
def series_delete(request, pk, template_name='cal/series_delete.html'):
	appointment = get_object_or_404(Appointment, pk=pk)
	series = get_object_or_404(Series, pk=appointment.series)

	if request.method == 'POST' and request.is_ajax:
		appointment.delete()
		series.delete()
		response = {}
		response['userName'] = request.user.username
		response['success'] = True
		response['data'] = 'Series successfully deleted'

		json_response = json.dumps(response)
		return HttpResponse(json_response, content_type="application/json")

	data = {}
	data['appointment'] = appointment
	data['series']  = series

	return render(request, template_name, data) 




@login_required
def calshare_create(request, template_name='cal/generic_form.html'):
	user = request.user.username
	form = CalShareForm(request.POST or None, user=user)
	if form.is_valid() and request.method == "POST" and request.is_ajax:
		calshare = form.save()

		response = {}
		response['userName'] = user
		response['success'] = True
		response['data'] = 'Calendar Share successfully created'

		json_response = json.dumps(response)
		return HttpResponse(json_response, content_type="application/json")

	return render(request, template_name, {'form':form})

