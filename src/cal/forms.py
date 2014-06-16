from django.forms import ModelForm

from cal.models import Calendar

class CalendarForm(ModelForm):
	class Meta:
		model = Calendar
		exclude = ['calendar_owner']
