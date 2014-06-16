from django.forms import ModelForm, ModelChoiceField, CharField
from django.contrib.auth.models import User
from cal.models import Calendar, Appointment, Series, CalendarShare

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

class CalShareForm(ModelForm):
	
	share_with = ModelChoiceField(queryset=User.objects.all())	

	def __init__(self, user, *args, **kwargs):
		super(CalShareForm, self).__init__(*args, **kwargs)
		usero = User.objects.get(username__exact=user)
		self.fields['calendar'].queryset = Calendar.objects.filter(calendar_owner=usero)
	
	class Meta:
		model = Appointment		
		fields = ['calendar', 'share_with']
		


				
