from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.main, name='main'),
    path('home-owner/', views.ownerLogin, name='ownerLogin'),
    path('owner_dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('ownerLogout/', views.ownerLogout, name='ownerLogout'),
    path('Secretary/', views.secretaryLogin, name='secretaryLogin'),
    path('Admin/', views.adminLogin, name='adminLogin'),
    path('adminLogout/', views.adminLogout, name='adminLogout'),
    path('register/', views.register, name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('ar/', views.ar_view, name='ar_view'),
]


