from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from USERS.models import HomeOwner, Resident
from .models import Secretary, Event, Comment, Property, Message
from USERS.forms import HomeOwnerForm, UserForm
from HOMEOWNER.forms import ResidentForm
from .forms import SecretaryForm, EditOwnerForm, PropertyForm, EventForm
from django.contrib import messages
from HOMEOWNER.models import Maintenance_request
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def admin_dashboard(request):
    totalHomeowners = HomeOwner.objects.filter(pending=False).count
    totalPendings = HomeOwner.objects.filter(pending=True).count
    maintenances = Maintenance_request.objects.order_by('-date_requested')[:5]
    events = Event.objects.all().order_by('-date_created')[:3]
    totalProperties = Property.objects.all().count
    occupied_properties = Property.objects.filter(availability='occupied')
    return render(request, 'admin_dashboard.html', {'totalPendings':totalPendings, 'maintenances':maintenances, 'events':events, 'totalProperties':totalProperties, 'totalHomeowners':totalHomeowners, 'occupied_properties':occupied_properties})

@login_required
def homeowners(request):
    message = request.GET.get('message', None)
    homeowners = HomeOwner.objects.filter(pending=False).all()
    paginator = Paginator(homeowners, 6)  # Show 6 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    owner = get_object_or_404(User, username=request.user)
    owner_property = 'None'
    if Property.objects.filter(household_head=owner).exists():
        owner_property = Property.objects.get(household_head=owner)

    total_household_members = Resident.objects.filter(household_representative=owner).all().count()
    return render(request, 'homeowners.html', {'homeowners':homeowners, 'message':message, 'page_obj':page_obj, 'paginator':paginator, 'owner_property':owner_property, 'total_household_members':total_household_members})

@login_required
def maintenance_request_list(request):
    total_maintenance_req = Maintenance_request.objects.all()
    paginator = Paginator(total_maintenance_req, 5)  # Show 5 requests per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'maintenance_request_list.html', {'page_obj': page_obj})

@login_required
def secretaries(request):
    message = request.GET.get('message', None)
    Secretaries = Secretary.objects.all()
    paginator = Paginator(Secretaries, 5)  # Show 5 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'secretaries.html', {'message':message, 'page_obj':page_obj})

@login_required
def residents(request):
    message = request.GET.get('message', None)
    residents = Resident.objects.all()
    paginator = Paginator(residents, 5)  # Show 5 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'residents.html', {'message':message, 'page_obj':page_obj,})

@login_required
def new_resident(request):
    mess = ''
    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            form.save()
            mess = 'Resident added successfully!'
    else:
        form = ResidentForm()
    return render(request, 'new_resident.html', {'form':form, 'mess':mess})

@login_required
def pending_accounts(request):
    message = request.GET.get('message')
    pendings = HomeOwner.objects.filter(pending=True)
    paginator = Paginator(pendings, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pending_accounts.html', {'pendings':pendings, 'page_obj':page_obj, 'message':message})


def messages(request):
	return render(request, 'messages.html')

def admin_get_pending_registrations(request):
    if request.method == 'GET':
        count = HomeOwner.objects.filter(pending=True).count()  # Adjust query according to your model
        return JsonResponse({'count': count})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def admin_mark_messages_as_read(request):
    if request.method == 'POST':
        # Perform your logic to mark messages as read
        HomeOwner.objects.filter(pending=True).update(status='read')
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def acceptPending(request, pk):
    pendingAccount = get_object_or_404(HomeOwner, pk=pk)
    pendingAccount.pending = False
    account_email = pendingAccount.user.email
    account_firstname = pendingAccount.user.first_name
    pendingAccount.save()

    send_account_accepted_email(account_email, account_firstname)

    return redirect('/pending_accounts/?message=Account accepted.')

def send_account_accepted_email(homeowner_email, firstname):
    subject = 'Housing Management System'
    message = f"Hello {firstname}, Your account has been accepted. You can now log in and manage your household."
    from_email = settings.DEFAULT_FROM_EMAIL
    recepient_list = [homeowner_email]

    send_mail(subject, message, from_email, recepient_list)


@login_required
def new_secretary(request):
    mess = ''
    if request.method == 'POST':
        form = SecretaryForm(request.POST)
        if form.is_valid():
            # Check if email or username already exists
            email_address = form.cleaned_data['email_address']
            user_name = form.cleaned_data['user_name']
            password = form.cleaned_data['password']

            if Secretary.objects.filter(email_address=email_address).exists():
                form.add_error('email_address', 'This email is already taken.')
            elif Secretary.objects.filter(user_name=user_name).exists():
                form.add_error('user_name', 'This username is already taken.')
            else:
                user = User.objects.create_user(
                    username = user_name,
                    email = email_address,
                    password = password,
                )
                user.save()
                secretary = form.save(commit=False)
                secretary.user = user
                secretary.save()
                mess = 'Registered succesfully!'
    else:
        form = SecretaryForm()
    
    return render(request, 'add_secretary.html', {'form': form, 'mess':mess})

@login_required
def new_homeowner(request):
    message = request.GET.get('message', None)
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
                        pending=False,
                    )
                    
                    homeowner.save()
                    mess = 'Homeowner created successfully!'
                    return redirect('/new_homeowner/?message=Owner created successfully!')
    else:
        form = UserForm()

    return render(request, 'add_homeowner.html', {'form': form, 'message':message})

def delete_owner(request, pk):
    if request.method == 'POST':
        user_to_del = HomeOwner.objects.get(pk=pk)
        user_to_del.delete()
        return redirect('/homeowners/?message=Deleted successfully!')

def edit_owner(request, pk):
    user = HomeOwner.objects.get(pk=pk)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        contact_number = request.POST.get('contact_number')
        email_address = request.POST.get('email')
        occupation = request.POST.get('occupation')

        if first_name and last_name and age and gender and contact_number and email_address and occupation:
            user.user.first_name = first_name
            user.user.last_name = last_name
            user.age = age
            user.gender = gender
            user.contact_number = contact_number
            user.user.email = email_address
            user.occupation = occupation
            user.save()
            return redirect('/homeowners/?message=Updated successfully!')

def delete_secretary(request, pk):
    secretary = Secretary.objects.get(pk=pk)
    secretary.delete()
    return redirect('/secretaries/?message=Secretary deleted  successfully!')

def edit_secretary(request, pk):
    secretary = Secretary.objects.get(pk=pk)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_number = request.POST.get('contact_number')
        email_address = request.POST.get('email_address')
        user_name = request.POST.get('user_name')

        if first_name and last_name and contact_number and email_address and user_name:
            secretary.first_name = first_name
            secretary.last_name = last_name
            secretary.contact_number = contact_number
            secretary.email_address = email_address
            secretary.user_name = user_name
            secretary.save()
            return redirect('/secretaries/?message=Secretary updated succesfully!')

@login_required
def maintenance_request_list(request):
    total_maintenance_req = Maintenance_request.objects.all()
    paginator = Paginator(total_maintenance_req, 5)  # Show 10 requests per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'maintenance_request_list.html', {'page_obj': page_obj})

def change_to_onGoing(request, pk):
    if request.method == 'POST':
        req = get_object_or_404(Maintenance_request, pk=pk)
        req.status = 'On going'
        req.save()
        return redirect('maintenance_request_list')

def change_to_done(request, pk):
    if request.method == 'POST':
        req = get_object_or_404(Maintenance_request, pk=pk)
        req.status = 'Done'
        req.save()
        return redirect('maintenance_request_list')

@login_required
def events(request):
    events = Event.objects.all().order_by('-event_date')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/events/?message=Event created successfully!')
    else:
        form = EventForm()

    return render(request, 'events.html', {'events':events, 'form':form})

@login_required
def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    comments = Comment.objects.filter(event=event).order_by('-date_commented')
    return render(request, 'event_detail.html', {'event':event, 'comments':comments})

def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_description = request.POST.get('event_description')
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')

        event.event_name=event_name
        event.event_description=event_description
        event.event_date=event_date
        event.event_time=event_time

        if 'image' in request.FILES:
            event.image=request.FILES('image')
        else:
            event.image=event.image

        event.save()
        return redirect('events')

def delete_event(request, pk):
    if request.method == 'POST':
        del_event = Event.objects.get(pk=pk)
        del_event.delete()

        return redirect('events')

def add_owner_comment(request, pk):
    if request.method == 'POST':
        event = Event.objects.get(pk=pk)
        owner_commenter = request.POST.get('owner_commentor')
        event_name = event.event_name
        comment = request.POST.get('comment')

        if owner_commenter and comment:
            new_comment = Comment.objects.create(
                owner_commenter=owner_commenter,
                event=event_name,
                comment=comment,
            )
            new_comment.save()
            return redirect(reverse('owner_event_detail', args=[pk]))

@login_required
def properties(request):
    message = request.GET.get('message', None)
    properties = Property.objects.all()
    return render(request, 'properties.html', {'properties':properties, 'message':message})

@login_required
def edit_property(request, pk):
    if request.method == 'POST':
        property_name = request.POST.get('property_name')
        block_number = request.POST.get('block_no')
        house_number = request.POST.get('lot_no')
        property_description = request.POST.get('property_description')
        
        if block_number and house_number:
            prop = Property.objects.get(pk=pk)
            prop.property_name = property_name
            prop.property_block_no = block_number
            prop.property_house_no = house_number
            prop.property_description = property_description
            prop.save()
            return redirect('/properties/?message=Property update successfully!')

def delete_property(request, pk):
    if request.method == 'POST':
        del_property = Property.objects.get(pk=pk)
        del_property.delete()
        return redirect('/properties/?message=Property deleted succesfully!')

@csrf_exempt
def admin_get_new_messages(request):
    if request.method == 'GET':
        messages = Message.objects.all().order_by('-sent_time')[:20]  # Adjust to your needs
        messages_list = [{
            'sender': msg.sender,  # Adjust the field based on your model
            'message': msg.message,
            'created_at': msg.sent_time
        } for msg in messages]
        return JsonResponse(messages_list, safe=False)

def get_profile_message(sender_username):
    try:
        user = User.objects.get(username=sender_username)
        homeowner = HomeOwner.objects.get(user=user)
        return homeowner.profile_picture.url if homeowner.profile_picture else None
    except HomeOwner.DoesNotExist:
        return None

@login_required
def admin_messages(request):
    messages = Message.objects.all()
    messages_with_pictures = []

    for message in messages:
        profile_picture_url = get_profile_message(message.sender)
        messages_with_pictures.append({
            'message': message,
            'profile_picture_url': profile_picture_url,
        })

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            new_message = Message.objects.create(
                sender=request.user.username,
                message=message
            )
            new_message.save()
            return redirect('admin_messages')

    return render(request, 'admin_messages.html', {'messages_with_pictures':messages_with_pictures,})


def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/properties/?message=New property added.')
    else:
        form = PropertyForm()
    return render(request, 'add_property.html', {'form':form})
