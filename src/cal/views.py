from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.utils import simplejson
from cal.models import Calendar
from cal.forms import CalendarForm
from django.http import HttpResponse
from cal.serializer import CalSerializer

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
def calendar_create(request, template_name='calendar/calendar_form.html'):
	form = CalendarForm(request.POST or none)
	if form.is_valid():
		calendar = form.save(commit=False)
		calendar.calendar_owner = request.user
		calendar.save()

		return redirect('calendar_view', pk=calendar.id)

	return render(request, template_name, {'form':form})


@login_required
def calendar_update(request, pk, template_name='calendar/calendar_form.html'):
        calendar = get_object_or_404(Adress, pk=pk)
        form = AdressForm(request.POST or None, instance=calendar)
        if form.is_valid():
                form.save()
                return redirect('calendar_list')

        return render(request, template_name, {'form':form})

@login_required
def calendar_delete(request, pk, template_name='calendar/calendar_delete.html'):
        calendar = get_object_or_404(Calendar, pk=pk)
        if request.method=='POST':
                calendar.delete()
                return redirect('calendar_list')

        return render(request, template_name, {'object':calendar})

