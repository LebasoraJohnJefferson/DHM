from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect 
from .models import HomeOwner, Resident
from HOMEOWNER.models import Activitie, Maintenance_request
from .forms import UserForm, HomeOwnerForm, OwnerLoginForm, SecretaryLoginForm
from ADMIN.models import Secretary, Event
from django.contrib import messages
from HOMEOWNER.models import Notification

# Create your views here.
def main(request):
	return render(request, 'main.html')

def register(request):
    mess = ''
    if request.method == 'POST':
        form = UserForm(request.POST)

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        if first_name == '':
            form.add_error('first_name', 'This field is required.')
        if last_name == '':   
            form.add_error('last_name', 'This field is required.')
        if email == '':
            form.add_error('email', 'This field is required.')
        else:
            if form.is_valid():
                    user = form.save()
                    homeowner = HomeOwner.objects.create(
                        user = user,
                        pending=True,
                    )
                    
                    homeowner.save()
                    messages.success(request, 'Your account has been created and is pending approval by the admin.')
                    return redirect('register')
    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form, 'mess':mess})


def ownerLogin(request):
    message = request.GET.get('message', None)
    username = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if HomeOwner.objects.filter(user=user).exists():
            if user is not None:
                homeowner = HomeOwner.objects.get(user=user)
                if homeowner.pending == False:
                    login(request, user)
                    messages.success(request, 'Login successfully!')
                    return redirect('owner_dashboard')
                else:
                    messages.warning(request, 'Your account is in pending approval')
            else:
                    messages.error(request, 'Incorrect credentials')
        else:
                 messages.error(request, 'Incorrect credentials')
    return render(request, 'ownerLogin.html', {'message':message, 'username':username})

@login_required
def owner_dashboard(request):
    try:
        user = User.objects.get(username=request.user)
        homeowner = HomeOwner.objects.get(user=user)
        profile = homeowner.profile_picture.url
        totalResidents = Resident.objects.filter(household_representative=user).all()
        totalMaintenanceReq = Maintenance_request.objects.filter(name_of_owner=user).all()
        activities = Activitie.objects.filter(name_of_owner=user).all().order_by('-date')
        events = Event.objects.all()
        notifications = Notification.objects.filter(homeowner=user).order_by('-created_at')
    except HomeOwner.DoesNotExist:
        homeowner = None
        profile = None
        activities = None
        totalResidents = None
        totalMaintenanceReq = None
        events = None
        notifications = None
    return render(request, 'owner_dashboard.html', {'profile':profile, 'activities':activities, 'totalResidents':totalResidents, 'totalMaintenanceReq':totalMaintenanceReq, 'events':events, 'notifications':notifications,})

def ownerLogout(request):
    logout(request)
    return redirect('main')

def secretaryLogin(request):
    message = request.GET.get('message', None)
    username = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if Secretary.objects.filter(user=user).exists():
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successfully!')
                return redirect('secretary_dashboard')
            else:
                messages.error(request, 'Incorrect credentials.')
        else:
            messages.error(request, 'Incorrect credentials.')
    return render(request, 'secretaryLogin.html', {'message':message, 'username':username})

def adminLogin(request):
    mess = ''
    username = ''
    password = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            mess = 'Both username and password are required.'
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_superuser:
                    login(request, user)
                    return redirect('admin_dashboard')  # Replace 'admin_dashboard' with your actual admin dashboard URL name
                else:
                    mess = 'You are not authorized to access the admin area'
            else:
                mess = 'Invalid username or password'

    return render(request, 'adminLogin.html', {'mess': mess, 'username':username, 'password':password})

def adminLogout(request):
    logout(request)
    return redirect('main')
	

def ar_view(request):
    return render(request, 'arMap.html')

