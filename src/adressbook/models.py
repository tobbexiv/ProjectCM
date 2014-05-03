from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Adress(models.Model):
	name = models.CharField(max_length=60, null=False, blank=False)
	picture = models.CharField(max_length=180)
	street = models.CharField(max_length=120)
	house_nr = models.IntegerField()
	zip_code = models.IntegerField()
	town_name = models.CharField(max_length=120)
	country = models.CharField(max_length=60)
	telephone_nr = models.IntegerField()
	email = models.EmailField(max_length=60, null=False, blank=False)
	contact_owner = models.ForeignKey(User)

	def __str__(self):
		pass
