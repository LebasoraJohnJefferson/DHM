from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('secretary_dashbord/', views.secretary_dashboard, name='secretary_dashboard'),
    path('sec_homewowners/', views.sec_homeowners, name='sec_homeowners'),
	path('sec_edit_owner/<int:pk>', views.sec_edit_owner, name='sec_edit_owner'),
	path('sec_homeowner_detail/<int:pk>/', views.sec_homeowner_detail, name='sec_homeowner_detail'),
	path('sec_new_homeowner/', views.sec_new_homeowner, name='sec_new_homeowner'),
	path('sec_properties/', views.sec_properties, name='sec_properties'),
	path('sec_edit_property/<int:pk>', views.sec_edit_property, name='sec_edit_property'),
	path('sec_delete_property/<int:pk>', views.sec_delete_property, name='sec_delete_property'),
	path('sec_add_property/', views.sec_add_property, name='sec_add_property'),
	path('sec_maintenance_request_list/', views.sec_maintenance_request_list, name='sec_maintenance_request_list'),
    path('sec_get_maintenances/', views.sec_get_maintenances, name='sec_get_maintenances'),
	path('sec_change_to_done/<int:pk>', views.sec_change_to_done, name='sec_change_to_done'),
	path('sec_change_to_onGoing/<int:pk>', views.sec_change_to_onGoing, name='sec_change_to_onGoing'),
	path('sec_residents/', views.sec_residents, name='sec_residents'),
	path('sec_new_resident/', views.sec_new_resident, name='sec_new_resident'),
	path('sec_edit_resident/<int:pk>', views.sec_edit_resident, name='sec_edit_resident'),
	path('sec_delete_resident/<int:pk>', views.sec_delete_resident, name='sec_delete_resident'),
	path('sec_pending_accounts/', views.sec_pending_accounts, name='sec_pending_accounts'),
	path('get_pending_registrations/', views.get_pending_registrations, name='get_pending_registrations'),
    path('mark_messages_as_read/', views.mark_messages_as_read, name='mark_messages_as_read'),
	path('sec_acceptPending/<int:pk>', views.sec_acceptPending, name='sec_acceptPending'),
	path('sec_events/', views.sec_events, name='sec_events'),
	path('sec_edit_event/<int:pk>/', views.sec_edit_event, name='sec_edit_event'),
	path('sec_event_detail/<int:pk>/', views.sec_event_detail, name='sec_event_detail'),
    path('sec_messages/', views.sec_messages, name='sec_messages'),
]



