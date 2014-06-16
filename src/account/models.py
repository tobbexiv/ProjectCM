from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

# User Profile to extend User model for storring additional information
class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name="profile")
	max_inbox_size = models.IntegerField(null=True, blank=True)
	max_no_mail_accounts = models.IntegerField(null=True, blank=True)
	max_no_calendars = models.IntegerField(null=True, blank=True)

	

# Post save trigger that is called after User creation to create corresponding UserProfile
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)		

post_save.connect(create_user_profile, sender=User)		