from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('admin dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('homeowners/', views.homeowners, name='homeowners'),
    path('secretaries/', views.secretaries, name='secretaries'),
    path('residents/', views.residents, name='residents'),
	path('new_resident/', views.new_resident, name='new_resident'),
    path('pending_accounts/', views.pending_accounts, name='pending_accounts'),
    path('admin_get_pending_registrations/', views.admin_get_pending_registrations, name='admin_get_pending_registrations'),
    path('admin_mark_messages_as_read/', views.admin_mark_messages_as_read, name='admin_mark_messages_as_read'),
    path('messages/', views.messages, name='messages'),
    path('acceptPending/<int:pk>/', views.acceptPending, name='acceptPending'),
    path('new secretary/', views.new_secretary, name='new_secretary'),
    path('new_homeowner/', views.new_homeowner, name='new_homeowner'),
    path('delete_owner/<int:pk>/', views.delete_owner, name='delete_owner'),
    path('delete_secretary/<int:pk>/', views.delete_secretary, name='delete_secretary'),
    path('edit_owner/<int:pk>/', views.edit_owner, name='edit_owner'),
    path('edit_secretary/<int:pk>/', views.edit_secretary, name='edit_secretary'),
    path('maintenance_request_list/', views.maintenance_request_list, name='maintenance_request_list'),
    path('change_to_onGoing/<int:pk>/', views.change_to_onGoing, name='change_to_onGoing'),
    path('change_to_done/<int:pk>/', views.change_to_done, name='change_to_done'),
    path('events/', views.events, name='events'),
	path('edit_event/<int:pk>/', views.edit_event, name='edit_event'),
	path('delete_event/<int:pk>/', views.delete_event, name='delete_event'),
    path('event_detail/<int:pk>/', views.event_detail, name='event_detail'),
    path('properties/', views.properties, name='properties'),
    path('edit_property/<int:pk>/', views.edit_property, name='edit_property'),
    path('delete_property/<int:pk>/', views.delete_property, name='delete_property'),
    path('admin_messages/', views.admin_messages, name='admin_messages'),
    path('admin_get_new_messages/', views.admin_get_new_messages, name='admin_get_new_messages'),
    path('add_property/', views.add_property, name='add_property'),
]






