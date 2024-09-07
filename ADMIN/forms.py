# forms.py
from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Secretary, Property, Event
from USERS.models import HomeOwner

class SecretaryForm(forms.ModelForm):
    class Meta:
        model = Secretary
        fields = ['first_name', 'last_name', 'date_of_birth', 'age', 'gender', 'contact_number', 'email_address', 'name_of_emergency_contact', 'relationship_to_secretary', 'emergency_contact_number', 'highest_educational_attainment', 'user_name', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'contact_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control'}),
            'name_of_emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'relationship_to_secretary': forms.Select(attrs={'class': 'form-control'}),
            'emergency_contact_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'highest_educational_attainment': forms.Select(attrs={'class': 'form-control'}),
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already taken.')

        return cleaned_data

class EditOwnerForm(forms.ModelForm):
    class Meta:
        model = HomeOwner
        fields = ['date_of_birth', 'age', 'contact_number', 'gender', 'relationship_to_household', 'occupation', 'block_number', 'house_number']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'relationship_to_household': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'block_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'house_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_name','photo', 'bedroom', 'bathroom', 'property_block_no', 'property_house_no', 'property_description', 'availability']
        widgets = {
            'property_name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'property_block_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'property_house_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathroom': forms.NumberInput(attrs={'class': 'form-control'}),
            'bedroom': forms.NumberInput(attrs={'class': 'form-control'}),
            'property_description': forms.Select(attrs={'class': 'form-control'}),
            'availability': forms.Select(attrs={'class': 'form-control'}),
        }   

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['image', 'event_name', 'event_time', 'event_description', 'event_date', 'location']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'event_name': forms.TextInput(attrs={'class': 'form-control'}),
            'event_description': forms.TextInput(attrs={'class': 'form-control'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
        