# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from .models import Maintenance_request, Notification
from ADMIN.models import Comment, Event
from USERS.models import HomeOwner
from django.contrib.auth.models import User

@receiver(post_save, sender=Maintenance_request)
def create_notification(sender, instance, created, **kwargs):
    if instance.status == 'Done':
        description = instance.Description_of_issue
        notification_message = f"Your maintenance request '{description}' has been completed. Click to verify and provide feedback."
        Notification.objects.create(
            homeowner=instance.name_of_owner,
            message=notification_message,
            maintenance_request=instance
        )
        print(instance)
        


# @receiver(post_save, sender=Comment)
# def create_comment_notification(sender, instance, **kwargs):
#     event = instance.event
#     commentor = instance.owner_commentor
#     homeowners = User.objects.all()  # Adjust this if you need to notify specific homeowners
#     message = f"{commentor.username} commented to the event: {event.event_name}"

#     for homeowner in homeowners:
#         Notification.objects.create(
#             homeowner=homeowner,
#             message=message,
#         )
