from django.contrib import admin
from . import views
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('add member/', views.add_member, name='add_member'),
    path('household members/', views.household_members, name='household_members'),
    path('edit_member/<int:pk>/', views.edit_member, name='edit_member'),
	path('delete_member/<int:pk>/', views.delete_member, name='delete_member'),
    path('update_picture/<int:pk>/', views.update_picture, name='update_picture'),
    path('maintenance_request/', views.maintenance_request, name='maintenance_request'),
	path('request_verification/', views.request_verification, name='request_verification'),
    path('request_maintenance_list/', views.request_maintenance_list, name='request_maintenance_list'),
    path('edit_request/<int:pk>', views.edit_request, name='edit_request'),
    path('delete_request/<int:pk>', views.delete_request, name='delete_request'),
    path('owner_events/', views.owner_events, name='owner_events'),
    path('owner_event_detail/<int:pk>/', views.owner_event_detail, name='owner_event_detail'),
    path('add_owner_comment/<int:pk>/', views.add_owner_comment, name='add_owner_comment'),
	path('property_selection/', views.property_selection, name='property_selection'),
	path('confirm_selection/<int:pk>/', views.confirm_selection, name='confirm_selection'),
    path('property_detail/', views.property_detail, name='property_detail'),
    path('notifications/', views.get_notifications, name='get_notifications'),
    path('notifications/mark-read/', views.mark_notifications_as_read, name='mark_notifications_as_read'),
    path('owner_messages/', views.owner_messages, name='owner_messages'),
    path('get_new_messages/', views.get_new_messages, name='get_new_messages'),
	path('mark_messages_as_read/', views.mark_messages_as_read, name='mark_messages_as_read'),
	path('owner_profile/', views.owner_profile, name="owner_profile"),
    path('owner_notifications/', views.owner_notifications, name="owner_notifications"),
	path('detect_intent/', views.detect_intent, name="detect_intent"),
	path('chatbot/', views.chatbot, name="chatbot"),
]



