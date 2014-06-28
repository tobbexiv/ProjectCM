from django.forms import ModelForm, ModelChoiceField, CharField
from django.contrib.auth.models import User
from cal.models import Calendar, Appointment, Series, CalendarShare

class CalendarForm(ModelForm):
	class Meta:
		model = Calendar
		exclude = ['calendar_owner']

class AppointmentForm(ModelForm):

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		super(AppointmentForm, self).__init__(*args, **kwargs)
		usero = User.objects.get(username__exact=user)
		self.fields['calendar'].queryset = Calendar.objects.filter(calendar_owner=usero)

	class Meta:
		model = Appointment
		exclude =['series']

class SeriesForm(ModelForm):
	class Meta:
		model = Series

class CalShareForm(ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user')
		calendar = kwargs.pop('calendar')
		super(CalShareForm, self).__init__(*args, **kwargs)
		usero = User.objects.get(username__exact=user)

		existingShares = CalendarShare.objects.filter(calendar=calendar)
		dont_show_user = []
		dont_show_user.append(usero.pk)
		for share in existingShares:
			dont_show_user.append(share.share_with.pk)
		
		self.fields['share_with'].queryset = User.objects.all().exclude(pk__in=dont_show_user)

	class Meta:
		model = CalendarShare
		fields = ['share_with']
		


				
