from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from USERS.models import HomeOwner, Resident
from ADMIN.models import Secretary, Event, Comment, Property, Message
from USERS.forms import HomeOwnerForm, UserForm
from ADMIN.forms import SecretaryForm, EditOwnerForm, PropertyForm, EventForm
from SECRETARY.forms import ResidentForm
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
def secretary_dashboard(request):
    message = request.GET.get('message', None)
    totalHomeowners = HomeOwner.objects.filter(pending=False).count
    totalPendings = HomeOwner.objects.filter(pending=True).count
    maintenances = Maintenance_request.objects.order_by('-date_requested')[:5]
    events = Event.objects.all().order_by('-date_created')[:3]
    totalProperties = Property.objects.all().count
    occupied_properties = Property.objects.filter(availability='occupied')
    secretary = Secretary.objects.get(user=request.user)
    profile = secretary.profile_picture.url

    return render(request, 'secretary_dashboard.html', {'totalPendings':totalPendings, 'maintenances':maintenances, 'events':events, 'totalProperties':totalProperties, 'totalHomeowners':totalHomeowners, 'occupied_properties':occupied_properties, 'profile':profile, 'message':message})

@login_required
def sec_homeowners(request):
    message = request.GET.get('message', None)
    homeowners = HomeOwner.objects.filter(pending=False).all()
    paginator = Paginator(homeowners, 6)  # Show 6 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    secretary = Secretary.objects.get(user=request.user)
    profile = secretary.profile_picture.url
    return render(request, 'sec_homeowners.html', {'homeowners':homeowners, 'message':message, 'page_obj':page_obj, 'paginator':paginator, 'profile':profile})

@login_required
def sec_homeowner_detail(request, pk):
    owner = HomeOwner.objects.get(pk=pk)
    secretary = Secretary.objects.get(user=request.user)
    profile = secretary.profile_picture.url
    household_members = Resident.objects.filter(household_representative=owner.user)

    if Property.objects.filter(household_head=owner.user).exists():
        property_details = Property.objects.get(household_head=owner.user)
    else:
        property_details = 'none'

    maintenances = Maintenance_request.objects.filter(name_of_owner=owner.user)
    return render(request, 'sec_homeowner_detail.html', {'owner':owner, 'household_members':household_members, 'property_details':property_details, 'maintenances':maintenances, 'profile':profile})


@login_required
def sec_maintenance_request_list(request):
    total_maintenance_req = Maintenance_request.objects.all()
    paginator = Paginator(total_maintenance_req, 5)  # Show 5 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    secretary = Secretary.objects.get(user=request.user)
    profile = secretary.profile_picture.url
    return render(request, 'sec_maintenance_request_list.html', {'page_obj': page_obj, 'profile':profile})

@login_required
def sec_residents(request):
    message = request.GET.get('message', None)
    residents = Resident.objects.all()
    paginator = Paginator(residents, 5)  # Show 5 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    secretary = Secretary.objects.get(user=request.user)
    profile = secretary.profile_picture.url
    return render(request, 'sec_residents.html', {'message':message, 'page_obj':page_obj, 'profile':profile})

@login_required
def sec_new_resident(request):
    mess = ''
    secretary = Secretary.objects.get(user=request.user)
    profile = secretary.profile_picture.url

    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            form.save()
            mess = 'Resident added successfully!'
    else:
        form = ResidentForm()
    return render(request, 'sec_new_resident.html', {'profile':profile, 'form':form, 'mess':mess})

def sec_edit_resident(request, pk):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_address = request.POST.get('email_address')
        contact_number = request.POST.get('contact_number')
        occupation = request.POST.get('occupation')

        if first_name and last_name and email_address and contact_number and occupation:
            resident = Resident.objects.get(pk=pk)
            resident.first_name=first_name
            resident.last_name=last_name
            resident.contact_number=contact_number
            resident.email_address=email_address
            resident.occupation=occupation
            resident.save()
            messages.success(request, 'Update saved!')
            return redirect('sec_residents')
    
def sec_delete_resident(request, pk):
     if request.method == 'POST':
        resident_to_delete = Resident.objects.get(pk=pk)
        resident_to_delete.delete()
        messages.success(request, 'Deleted successfully!')
        return redirect('sec_residents')
          

@login_required
def sec_pending_accounts(request):
    message = request.GET.get('message')
    pendings = HomeOwner.objects.filter(pending=True)
    paginator = Paginator(pendings, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    secretary = Secretary.objects.get(user=request.user)
    profile = secretary.profile_picture.url
    return render(request, 'sec_pending.html', {'pendings':pendings, 'page_obj':page_obj, 'message':message, 'profile':profile})

def get_pending_registrations(request):
    if request.method == 'GET':
        count = HomeOwner.objects.filter(pending=True).count()  # Adjust query according to your model
        return JsonResponse({'count': count})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def mark_messages_as_read(request):
    if request.method == 'POST':
        # Perform your logic to mark messages as read
        HomeOwner.objects.filter(pending=True).update(status='read')
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def sec_messages(request):
	return render(request, 'sec_messages.html')

def sec_acceptPending(request, pk):
    pendingAccount = get_object_or_404(HomeOwner, pk=pk)
    pendingAccount.pending = False
    account_email = pendingAccount.user.email
    account_firstname = pendingAccount.user.first_name
    pendingAccount.save()

    sec_send_account_accepted_email(account_email, account_firstname)
    messages.success(request, 'Owner account accepted!')
    return redirect('sec_pending_accounts')

def sec_send_account_accepted_email(homeowner_email, firstname):
    subject = 'BAYVIEW HOMES - Housing Management System'
    message = f"Hello {firstname}, Your account has been accepted. You can now log in and manage your household ."
    from_email = settings.DEFAULT_FROM_EMAIL
    recepient_list = [homeowner_email]

    send_mail(subject, message, from_email, recepient_list)



def sec_new_homeowner(request):
    mess = ''
    secretary = Secretary.objects.get(user=request.user)
    profile = secretary.profile_picture.url
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
                    return redirect('sec_homeowners')
    else:
        form = UserForm()

    return render(request, 'sec_new_homeowner.html', {'form': form, 'mess':mess, 'profile':profile})

def sec_delete_owner(request, pk):
    if request.method == 'POST':
        user_to_del = HomeOwner.objects.get(pk=pk)
        user_to_del.delete()
        messages.success(request, 'Deleted successfully!')
        return redirect('sec_homeowners')

def sec_edit_owner(request, pk):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_number = request.POST.get('contact_number')
        email_address = request.POST.get('email_address')
        occupation = request.POST.get('occupation')

        if first_name and last_name and contact_number and email_address and occupation:
            owner = get_object_or_404(HomeOwner, pk=pk)
            user = owner.user
            user.first_name = first_name
            user.last_name = last_name
            owner.contact_number = contact_number
            user.email = email_address
            owner.occupation = occupation
            user.save()
            owner.save()
            messages.success(request, 'Update saved!')
            return redirect('sec_homeowners')

def sec_delete_secretary(request, pk):
    secretary = Secretary.objects.get(pk=pk)
    secretary.delete()
    return redirect('/sec_secretaries/?message=Secretary deleted  successfully!')

@login_required
def sec_maintenance_request_list(request):
    total_maintenance_req = Maintenance_request.objects.all().order_by('-date_requested')
    paginator = Paginator(total_maintenance_req, 5)  # Show 10 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    secretary = Secretary.objects.get(user=request.user)
    profile = secretary.profile_picture.url
    return render(request, 'sec_maintenance_request_list.html', {'page_obj': page_obj, 'profile':profile})

def sec_get_maintenances(request):
    if request.method == 'GET':
        count = Maintenance_request.objects.filter(status='Pending').count()  # Adjust query according to your model
        return JsonResponse({'count': count})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def sec_change_to_onGoing(request, pk):
    if request.method == 'POST':
        req = get_object_or_404(Maintenance_request, pk=pk)
        req.status = 'On going'
        req.save()
        return redirect('sec_maintenance_request_list')

def sec_change_to_done(request, pk):
    if request.method == 'POST':
        req = get_object_or_404(Maintenance_request, pk=pk)
        req.status = 'Done'
        req.save()

        # Get the homeowner's email through the connected User model
        homeowner_user = req.name_of_owner  # Assuming `HomeOwner` has a `user` field linking to `User`
        homeowner_email = req.name_of_owner.email

        # Send email to the homeowner
        subject = 'Maintenance Request Completed'
        message = f"Hello {homeowner_user} Your maintenance request '{req.Description_of_issue}' has been done. Please log in and verify the completion."
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(
            subject,
            message,
            from_email,
            [homeowner_email],
            fail_silently=False,
        )

        return redirect('sec_maintenance_request_list')

@login_required
def sec_events(request):
    message = request.GET.get('message', None)
    events = Event.objects.all().order_by('-event_date')
    secretary = Secretary.objects.get(user=request.user)
    profile = secretary.profile_picture.url

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created successfully!')
            return redirect('sec_events')
    else:
        form = EventForm()

    return render(request, 'sec_events.html', {'events':events, 'form':form, 'profile':profile, 'message':message})

@login_required
def sec_event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    comments = Comment.objects.filter(event=event).order_by('-date_commented')
    return render(request, 'sec_event_detail.html', {'event':event, 'comments':comments})

def sec_edit_event(request, pk):
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
        messages.success(request, 'Event update saved!')
        return redirect('sec_events')

def sec_delete_event(request, pk):
    if request.method == 'POST':
        del_event = Event.objects.get(pk=pk)
        del_event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('sec_events')

# def sec_add_owner_comment(request, pk):
#     if request.method == 'POST':
#         event = Event.objects.get(pk=pk)
#         owner_commenter = request.POST.get('owner_commentor')
#         event_name = event.event_name
#         comment = request.POST.get('comment')

#         if owner_commenter and comment:
#             new_comment = Comment.objects.create(
#                 owner_commenter=owner_commenter,
#                 event=event_name,
#                 comment=comment,
#             )
#             new_comment.save()
#             return redirect(reverse('sec_event_detail', args=[pk]))

@login_required
def sec_properties(request):
    message = request.GET.get('message', None)
    properties = Property.objects.all()
    secretary = Secretary.objects.get(user=request.user)
    profile = secretary.profile_picture.url
    return render(request, 'sec_properties.html', {'properties':properties, 'message':message, 'profile':profile})

@login_required
def sec_edit_property(request, pk):
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
            messages.success(request, 'Property update saved!')
            return redirect('sec_properties')

def sec_delete_property(request, pk):
    if request.method == 'POST':
        del_property = Property.objects.get(pk=pk)
        del_property.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('sec_properties')

@csrf_exempt
def sec_get_new_messages(request):
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
def sec_messages(request):
    messages = Message.objects.all()
    secretary = Secretary.objects.get(user=request.user)
    profile = secretary.profile_picture.url
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
            return redirect('sec_messages')

    return render(request, 'sec_messages.html', {'messages_with_pictures':messages_with_pictures, 'profile':profile})

@login_required
def sec_add_property(request):
    message = request.GET.get('message', None)
    secretary = Secretary.objects.get(user=request.user)
    profile = secretary.profile_picture.url
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property added successfully!')
            return redirect('sec_properties')
    else:
        form = PropertyForm()
    return render(request, 'sec_add_property.html', {'form':form, 'profile':profile, 'message':message})
