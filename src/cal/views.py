from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
import json
from cal.models import Calendar
from cal.forms import CalendarForm

@login_required
def calendar_list(request, template_name='calendar/calendar_list.html'):
	calendar = Calendar.object.filter(calendar_owner=request.user)
	response = {}
	response['userName'] = request.username
	response['success'] = True
	response['data'] = calendar
	
	json_response = serializers.serialize('json', response)
	return render(request, template_name, json_response)

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

