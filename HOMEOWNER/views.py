from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ResidentForm
from django.contrib import messages
from USERS.models import HomeOwner, Resident
from USERS.forms import HomeOwnerForm, UserForm, EditUserForm
from .models import Maintenance_request, Activitie, Notification
from ADMIN.models import Event, Comment, Message, Property
from django.urls import reverse
from django.http import JsonResponse
from google.cloud import dialogflow_v2 as dialogflow
from django.views.decorators.http import require_POST
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import uuid

# Create your views here.
@login_required
def add_member(request):
    username = request.user
    user = User.objects.get(username=username)
    homeowner = HomeOwner.objects.get(user=user)
    notifications = Notification.objects.filter(homeowner=user).order_by('-created_at')
    profile = homeowner.profile_picture.url
    name_of_owner = user
    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=user)
            block_number = homeowner.block_number
            house_number = homeowner.house_number
            household_representative = user

            # Save the form instance without committing to the database
            resident = form.save(commit=False)
            # Set the additional fields
            resident.block_number = block_number
            resident.house_number = house_number
            resident.household_representative = household_representative
            # Save the instance to the database
            resident.save()

            # Update the total household members based on the actual count
            user.total_household_members = Resident.objects.filter(household_representative=user).count()
            user.save()

            new_act = Activitie.objects.create(
                name_of_owner = name_of_owner,
                name_of_activity = 'Added a new household member.'
            )
            new_act.save()

            messages.success(request, 'A member is added successfully!')
            return redirect('add_member')
        else:
            messages.error(request, 'Submit failed!')
    else:
        form = ResidentForm()

    return render(request, 'add_member.html', {'form': form, 'profile':profile, 'user':user, 'username':username, 'notifications':notifications,})

@login_required
def household_members(request):
    message = request.GET.get('message', None)
    user = User.objects.get(username=request.user)
    homeowner = HomeOwner.objects.get(user=user)
    notifications = Notification.objects.filter(homeowner=user).order_by('-created_at')
    profile = homeowner.profile_picture.url
    id = user.pk
    residents = Resident.objects.filter(household_representative=user).all()
    paginator = Paginator(residents, 6)  # Show 6 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'household_members.html', {'page_obj':page_obj, 'profile':profile, 'paginator':paginator, 'id':id, 'notifications':notifications, 'message':message})

def edit_member(request, pk):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_address = request.POST.get('email_address')
        contact_number = request.POST.get('contact_number')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        occupation = request.POST.get('occupation')
        relationship_to_household = request.POST.get('relationship_to_household')

        if first_name and last_name and email_address and contact_number and age and gender and occupation and relationship_to_household:
            member = get_object_or_404(Resident, pk=pk)
            member.first_name = first_name
            member.last_name = last_name
            member.email_address = email_address
            member.contact_number = contact_number
            member.age = age
            member.gender = gender
            member.occupation = occupation
            member.save()
            messages.success(request, 'Update saved')
            return redirect('household_members')

def delete_member(request, pk):
    if request.method == 'POST':
        member_delete = Resident.objects.get(pk=pk)
        member_delete.delete()
        messages.success(request, 'member deleted successfully!')
        return redirect('household_members')

def update_picture(request, pk):
    user = User.objects.get(username=request.user)
    homeowner = HomeOwner.objects.get(user=user)
    name_of_owner = user
    if request.method == 'POST' and 'picture' in request.FILES:
        picture = request.FILES['picture']
        user = User.objects.get(pk=pk)

        if picture:
            homeowner.profile_picture = picture
            homeowner.save()

            #to activities
            new_act = Activitie.objects.create(
                    name_of_owner = name_of_owner,
                    name_of_activity = 'Updated profile picture.'
                )
            new_act.save() 
            messages.success(request, 'Profile saved')
            return redirect('owner_dashboard')

@login_required
def maintenance_request(request):
    user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        name_of_owner = user
        description_of_issue = request.POST.get('description_of_issue')
        type_of_issue = request.POST.get('type_of_issue')
        location = request.POST.get('location_of_issue')

        if description_of_issue and type_of_issue and location:
            maintenance_req = Maintenance_request.objects.create(
                name_of_owner = name_of_owner,
                Description_of_issue = description_of_issue,
                type_of_issue = type_of_issue,
                location = location,
            )
            maintenance_req.save()

            messages.success(request, 'Request submitted')

            #to activities
            new_act = Activitie.objects.create(
                name_of_owner = name_of_owner,
                name_of_activity = 'Requested a maintenance.'
            )
            new_act.save()
            return redirect('owner_dashboard')
    else:
        return redirect('owner_dashboard')
    
def request_verification(request):
    if request.method == 'POST':
        request_pk = request.POST.get('request_pk')
        verification = request.POST.get('verification')
        feedback = request.POST.get('feedback')

        request = get_object_or_404(Maintenance_request, pk=request_pk)
        if verification and feedback:
            request.status=verification
            request.feedback=feedback
            request.save()
            return redirect('/owner_notifications/?message=Verfication submitted!')

@login_required
def request_maintenance_list(request):
    message = request.GET.get('message', None)
    user = User.objects.get(username=request.user)
    homeowner = HomeOwner.objects.get(user=user)
    notifications = Notification.objects.filter(homeowner=user).order_by('-created_at')
    profile = homeowner.profile_picture.url
    id = user.pk
    maintenance_requests = Maintenance_request.objects.filter(name_of_owner=user).all().order_by('-date_requested')
    paginator = Paginator(maintenance_requests, 5)  # Show 5 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'request_maintenance_list.html', {'page_obj':page_obj, 'paginator':paginator, 'profile':profile, 'id':id, 'notifications':notifications, 'message':message})

def edit_request(request, pk):
    if request.method == 'POST':
        description = request.POST.get('description')
        type_of_issue = request.POST.get('type_of_issue')
        location = request.POST.get('location')

        if description and type_of_issue and location:
            request_to_edit = Maintenance_request.objects.get(pk=pk)
            request_to_edit.Description_of_issue = description
            request_to_edit.type_of_issue = type_of_issue
            request_to_edit.location = location
            request_to_edit.save()
            messages.success(request, 'Update saved!')
            return redirect('request_maintenance_list')
        
def delete_request(request, pk):
    if request.method == 'POST':
        request_to_delete = Maintenance_request.objects.get(pk=pk)
        request_to_delete.delete()
        messages.success(request, 'Deleted successfully!')
        return redirect('request_maintenance_list')

@login_required
def owner_events(request):
    user_name = request.user
    user = User.objects.get(username=user_name)
    homeowner = HomeOwner.objects.get(user=user)
    notifications = Notification.objects.filter(homeowner=user).order_by('-created_at')
    profile = homeowner.profile_picture.url
    id = user.pk
    events = Event.objects.all()
    return render(request, 'owner_events.html', {'user_name':user_name, 'events':events, 'profile':profile, 'id':id, 'notifications':notifications,})

def owner_event_detail(request, pk):
    user = User.objects.get(username=request.user)
    homeowner = HomeOwner.objects.get(user=user)
    notifications = Notification.objects.filter(homeowner=user).order_by('-created_at')
    profile = homeowner.profile_picture.url
    id = user.pk
    event = Event.objects.get(pk=pk)
    comments = Comment.objects.filter(event=event).order_by('-date_commented')
    return render(request, 'owner_event_detail.html', {'event':event, 'profile':profile, 'id':id, 'comments':comments, 'notifications':notifications,})

def add_owner_comment(request, pk):
    if request.method == 'POST':
        event = Event.objects.get(pk=pk)
        owner_commentor_id = request.POST.get('owner_commentor')
        event_name = event.event_name
        comment = request.POST.get('comment')
        get_user = User.objects.get(pk=owner_commentor_id)
        homeowner = HomeOwner.objects.get(user=get_user)
        user_image = homeowner.profile_picture

        if owner_commentor_id and comment:
            # owner_commentor = get_object_or_404(HomeOwner, pk=owner_commentor_id)
            new_comment = Comment.objects.create(
                owner_commentor=get_user,
                event=event,
                comment=comment,
                image=user_image
            )
            new_comment.save()
            return redirect(reverse('owner_event_detail', args=[pk]))

@receiver(post_save, sender=Maintenance_request)
def create_notification(sender, instance, **kwargs):
    if instance.status == 'Done':  # Your condition for sending notification
        Notification.objects.create(
            homeowner=instance.name_of_owner,
            message='You maintenance request has been done.'
        )

@login_required
def property_selection(request):
    user = User.objects.get(username=request.user)
    homeowner = HomeOwner.objects.get(user=user)
    notifications = Notification.objects.filter(homeowner=user).order_by('-created_at')
    profile = homeowner.profile_picture.url
    id = user.pk
    available_properties = Property.objects.filter(availability='available')
    return render(request, 'property_selection.html', {'profile':profile, 'id':id, 'notifications':notifications, 'available_properties':available_properties})

@login_required
def confirm_selection(request, pk):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        selected_property = Property.objects.get(pk=pk)
        selected_property.household_head = user
        selected_property.availability = 'occupied'
        selected_property.save()
        return redirect('property_detail')

@login_required
def property_detail(request):
    user = User.objects.get(username=request.user)
    homeowner = HomeOwner.objects.get(user=user)
    notifications = Notification.objects.filter(homeowner=user).order_by('-created_at')
    profile = homeowner.profile_picture.url
    id = user.pk
    
    if Property.objects.filter(household_head=user).exists():
        my_property = Property.objects.get(household_head=user)
    else:
        my_property = None

    maintenance_history = Maintenance_request.objects.filter(name_of_owner=user).order_by('-date_requested')

    return render(request, 'property_detail.html', {'profile':profile, 'id':id, 'notifications':notifications, 'my_property':my_property, 'maintenance_history':maintenance_history})


def get_notifications(request):
    user = get_object_or_404(User, username=request.user)
    notifications = Notification.objects.filter(homeowner=user, is_read=False)
    notifications_data = list(notifications.values('id', 'message', 'created_at'))
    return JsonResponse(notifications_data, safe=False)

@require_POST
def mark_notifications_as_read(request):
    user = request.user
    user = get_object_or_404(User, username=user)
    Notification.objects.filter(homeowner=user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def get_new_messages(request):
    if request.method == 'GET':
        messages = Message.objects.filter(is_read=False).order_by('-sent_time')[:20]  # Adjust to your needs
        messages_list = [{
            'sender': msg.sender,  # Ensure this matches your Message model's sender field
            'message': msg.message,
            'created_at': msg.sent_time.strftime('%Y-%m-%d %H:%M:%S')
        } for msg in messages]
        return JsonResponse(messages_list, safe=False)

@csrf_exempt
def mark_messages_as_read(request):
    if request.method == 'POST':
        Message.objects.filter(is_read=False).update(is_read=True)
        return JsonResponse({'status': 'ok'})

def get_profile_message(sender_username):
    try:
        homeowner = HomeOwner.objects.get(user=sender_username)
        return homeowner.profile_picture.url if homeowner.profile_picture else None
    except HomeOwner.DoesNotExist:
        return None

@login_required
def owner_messages(request):
    user = User.objects.get(username=request.user)
    homeowner = HomeOwner.objects.get(user=user)
    user_name = request.user.username
    notifications = Notification.objects.filter(homeowner=user).order_by('-created_at')
    profile = homeowner.profile_picture.url
    id = user.pk

    messages = Message.objects.all()
    messages_with_pictures = []

    for message in messages:
        profile_picture_url = get_profile_message(request.user)
        messages_with_pictures.append({
            'message': message,
            'profile_picture_url': profile_picture_url,
        })

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            new_message = Message.objects.create(
                sender=user_name,
                message=message,
            )
            new_message.save()
            return redirect('owner_messages')

    return render(request, 'owner_messages.html', {'profile':profile, 'id':id, 'notifications':notifications, 'messages_with_pictures':messages_with_pictures})


def owner_profile(request):
    message = request.GET.get('message', None)
    user = User.objects.get(username=request.user)
    homeowner = HomeOwner.objects.get(user=user)
    notifications = Notification.objects.filter(homeowner=user).order_by('-created_at')
    profile = homeowner.profile_picture.url

    if Property.objects.filter(household_head=user).exists():
        my_property = Property.objects.get(household_head=user)
    else:
        my_property = 'None'

    id = user.pk

    if request.method == 'POST':
        userForm = EditUserForm(request.POST, instance=user)
        ownerForm = HomeOwnerForm(request.POST, request.FILES, instance=homeowner)
        
        # Debugging: Print form errors
        if userForm.is_valid() and ownerForm.is_valid():
            userForm.save()
            ownerForm.save()
            mess = 'Edited successfully!'
            return redirect('/owner_profile/?message=Update saved!')
        else:
            mess = 'Error'
            print("User Form Errors: ", userForm.errors)
            print("Owner Form Errors: ", ownerForm.errors)
    else:
        userForm = EditUserForm(instance=user)
        ownerForm = HomeOwnerForm(instance=homeowner)

    return render(request, 'owner_profile.html', {
        'profile': profile,
        'id': id,
        'notifications': notifications,
        'homeowner': homeowner,
        'my_property': my_property,
        'userForm': userForm,
        'ownerForm': ownerForm,
        'message': message,
    })


def owner_notifications(request):
    message = request.GET.get('message', None)
    user = User.objects.get(username=request.user)
    homeowner = HomeOwner.objects.get(user=user)
    notifications = Notification.objects.filter(homeowner=request.user).select_related('maintenance_request').order_by('-created_at')
    profile = homeowner.profile_picture.url

    return render(request, 'owner_notifications.html', {
        'profile': profile,
        'id': id,
        'notifications': notifications,
        'homeowner': homeowner,
        'message': message,
    })

def chatbot(request):
    return render(request, 'chatbot.html')

def detect_intent(request):
    text = request.GET.get('query', '')
    print(f"Received query: {text}")  # Debugging

    if 'session_id' not in request.session:
        request.session['session_id'] = str(uuid.uuid4())

    session_id = request.session['session_id']
    print(f"Session ID: {session_id}")  # Debugging

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path('dynamic-cooler-434604-i2', session_id)

    text_input = dialogflow.TextInput(text=text, language_code='en')
    query_input = dialogflow.QueryInput(text=text_input)
    
    try:
        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
        print(f"Dialogflow response: {response.query_result.fulfillment_text}")
    except Exception as e:
        print(f"Error: {e}")  # General error
        import traceback
        traceback.print_exc()  # This will print the full error stack trace
        return JsonResponse({'response': 'Sorry, something went wrong.'})


    return JsonResponse({'response': response.query_result.fulfillment_text})
