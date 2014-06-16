from django.forms import ModelForm

from cal.models import Calendar, Appointment, Series

class CalendarForm(ModelForm):
	class Meta:
		model = Calendar
		exclude = ['calendar_owner']

class AppointmentForm(ModelForm):
	class Meta:
		model = Appointment
		exclude =['series']

class SeriesForm(ModelForm):
	class Meta:
		model = Series
				
