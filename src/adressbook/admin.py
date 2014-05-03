from django.contrib import admin

# Register your models here.



#------------------------------------------------
## For test use only:

from .models import Adress
#
class AdressbookAdmin(admin.ModelAdmin):
	class Meta:
		model = Adress

admin.site.register(Adress, AdressbookAdmin)

#------------------------------------------------
