from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Adress(models.Model):
	name = models.CharField(max_length=60, null=False, blank=False)
	picture = models.CharField(max_length=180, null=True, blank=True)
	street = models.CharField(max_length=120, null=True, blank=True)
	house_nr = models.IntegerField(null=True, blank=True)
	zip_code = models.IntegerField(null=True, blank=True)
	town_name = models.CharField(max_length=120, null=True, blank=True)
	country = models.CharField(max_length=60, null=True, blank=True)
	telephone_nr = models.IntegerField(null=True, blank=True)
	email = models.EmailField(max_length=60, null=False, blank=False)
	contact_owner = models.ForeignKey(User)

	def __str__(self):
		return self.name
