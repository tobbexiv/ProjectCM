from django.contrib import admin

# Register your models here

from .models import Calendar, Appointment, ShareRights, AppointmentShare, CalendarShare, Series

class CalendarAdmin(admin.ModelAdmin):
	class Meta:
		model = Calendar
admin.site.register(Calendar, CalendarAdmin)

class AppointmentAdmin(admin.ModelAdmin):
	 class Meta:
                model = Appointment
admin.site.register(Appointment, AppointmentAdmin)

class ShareRightsAdmin(admin.ModelAdmin):
	 class Meta:
                model = ShareRights
admin.site.register(ShareRights, ShareRightsAdmin)

class AppointmentShareAdmin(admin.ModelAdmin):
	 class Meta:
                model = AppointmentShare
admin.site.register(AppointmentShare, AppointmentShareAdmin)

class CalendarShareAdmin(admin.ModelAdmin):
	 class Meta:
                model = CalendarShare
admin.site.register(CalendarShare, CalendarShareAdmin)

class SeriesAdmin(admin.ModelAdmin):
	 class Meta:
                model = Series
admin.site.register(Series, SeriesAdmin)

