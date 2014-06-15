from django.forms import ModelForm


class CalendarForm(ModelForm):
	class Meta:
		model = Calendar
		exclude = ['calendar_owner']
