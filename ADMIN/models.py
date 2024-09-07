from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from HOMEOWNER.models import HomeOwner
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here
class Secretary(models.Model):
	gender_choices = [
		('male', 'Male'),
		('female', 'Female'),
	]

	relationship_choices = [
		('mother', 'Mother'),
		('father', 'Father'),
		('son', 'Son'),
		('daugter', 'Daughter'),
		('others', 'Others'),
	]

	educational_choices = [
		('elementary' ,'Elementary'),
		('highschool' ,'Highschool'),
		('college' ,'College'),
	]

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	role = models.CharField(max_length=255, default='secretary')
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	date_of_birth = models.DateField()
	age = models.IntegerField(default=0)
	gender = models.CharField(max_length=255, choices=gender_choices)
	contact_number = models.IntegerField()
	email_address = models.CharField(max_length=255)
	name_of_emergency_contact = models.CharField(max_length=255)
	relationship_to_secretary = models.CharField(max_length=255, choices=relationship_choices)
	emergency_contact_number = models.IntegerField()
	highest_educational_attainment = models.CharField(max_length=255, choices=educational_choices)
	user_name = models.CharField(max_length=255)
	password = models.CharField(max_length=128)
	profile_picture = models.ImageField(default='secretary.png')


	def set_password(self, raw_password):
		self.password = make_password(raw_password)
		self.save()

	def check_password(self, raw_password):
		return check_password(raw_password, self.password)

	def __str__(self):
		return self.user_name

	class Meta:
		verbose_name_plural = 'Secretaries'


class Event(models.Model):
	event_name = models.CharField(max_length=255)
	event_description = models.TextField()
	event_date = models.DateField()
	event_time = models.TimeField()
	date_created = models.DateField(auto_now_add=True)
	location = models.CharField(max_length=255)
	image = models.ImageField(default='events.jpg')

	def __str__(self):
		return self.event_name


class Comment(models.Model):
	owner_commentor = models.ForeignKey(User, on_delete=models.CASCADE)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	comment = models.TextField()
	date_commented = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(default='events.jpg')

	def __str__(self):
		return self.comment


class Message(models.Model):
	message = models.TextField()
	sender = models.CharField(max_length=255)
	sent_time = models.DateTimeField(auto_now_add=True)
	is_read = models.BooleanField(default=False)
	

	def __str__(self):
		return self.sender


class NonSuperUserManager(models.Manager):
		def get_queryset(self):
			return super().get_queryset().filter(is_superuser=False)
		
class NonSuperUser(User):
	objects = NonSuperUserManager()
	class Meta:
		proxy = True
	
class Property(models.Model):
	description = (
		('single', 'Single'),
		('double', 'Double'),
		('family', 'Family'),
	)
	availability_choices = (
		('available', 'Available'),
		('occupied', 'Occupied'),
		('under_maintenance', 'Under maintenance'),
	)

	#household information
	household_head = models.OneToOneField(NonSuperUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='household_head')
	property_name = models.CharField(max_length=255, default='house name')
	contact_no = models.IntegerField(null=True, blank=True)
	photo = models.ImageField(default="pope-francis-village.png")
	#property detail
	property_block_no = models.IntegerField()
	property_house_no = models.IntegerField(unique=True)
	property_description = models.CharField(max_length=255, choices=description)
	bathroom = models.IntegerField(default=0)
	bedroom = models.IntegerField(default=0)
	availability = models.CharField(max_length=255, choices=availability_choices, default="available")
	date_registered = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.property_description
	
	class Meta:
		verbose_name_plural = 'Properties'

