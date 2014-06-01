from django.contrib import admin

# Register your models here.

#------------------------------------------------
## For test use only:
from .models import MailAccount, MailHost

class MailAccoutAdmin(admin.ModelAdmin):
 	class Meta:
 		model = MailAccount

admin.site.register(MailAccount, MailAccoutAdmin)

class MailHostAdmin(admin.ModelAdmin):
 	class Meta:
 		model = MailHost

admin.site.register(MailHost, MailHostAdmin)



#------------------------------------------------
