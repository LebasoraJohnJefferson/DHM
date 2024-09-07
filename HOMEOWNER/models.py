from django.db import models
from USERS.models import HomeOwner
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
class Maintenance_request(models.Model):
	name_of_owner = models.ForeignKey(User, on_delete=models.CASCADE)
	Description_of_issue = models.TextField()
	type_of_issue = models.CharField(max_length=255)
	location = models.CharField(max_length=255)
	status = models.CharField(max_length=255, blank=True, default='Pending')
	date_requested = models.DateTimeField(auto_now_add=True, blank=True)
	feedback = models.TextField(blank=True, null=True)  # New field for feedback

	def __str__(self):
		return self.Description_of_issue

class Activitie(models.Model):
	name_of_owner = models.ForeignKey(User, on_delete=models.CASCADE)
	name_of_activity = models.CharField(max_length=255)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name_of_activity

class Notification(models.Model):
	homeowner = models.ForeignKey(User, on_delete=models.CASCADE)
	message = models.TextField()
	is_read = models.BooleanField(default=False)
	created_at = models.DateTimeField(default=timezone.now)
	maintenance_request = models.ForeignKey(Maintenance_request, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.message
	
