# forms.py
from django import forms
from django.contrib.auth.hashers import make_password
from .models import HomeOwner
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password1"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50'}),
            'first_name': forms.TextInput(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50'}),
            'last_name': forms.TextInput(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50'}),
            'email': forms.TextInput(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50'}),
            'password1': forms.PasswordInput(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50', 'placeholder': 'password'}),
            'password2': forms.PasswordInput(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50', 'placeholder': 'confirm password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get("password_confirm")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50'}),
            'last_name': forms.TextInput(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50'}),
            'email': forms.EmailInput(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50'}),
        }

# class HomeOwnerForm(forms.ModelForm):
#     class Meta:
#         model = HomeOwner
#         fields = ['suffix', 'date_of_birth', 'age', 'contact_number', 'sr_citizen', 'gender', 'place_of_birth', 'civil_status', 'religion', 'pwd', 'pregnant', 'relationship_to_household', 'previous_address', 'highest_educational_attainment', 'occupation', 'registration_date', 'block_number', 'house_number','profile_picture']
#         widgets = {
#             'suffix': forms.TextInput(attrs={'class': 'form-control'}),
#             'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
#             'age': forms.NumberInput(attrs={'class': 'form-control'}),
#             'contact_number': forms.NumberInput(attrs={'class': 'form-control'}),
#             'sr_citizen': forms.Select(attrs={'class': 'form-control'}),
#             'gender': forms.Select(attrs={'class': 'form-control'}),
#             'place_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
#             'civil_status': forms.Select(attrs={'class': 'form-control'}),
#             'religion': forms.Select(attrs={'class': 'form-control'}),
#             'pwd': forms.Select(attrs={'class': 'form-control'}),
#             'pregnant': forms.Select(attrs={'class': 'form-control'}),
#             'relationship_to_household': forms.Select(attrs={'class': 'form-control'}),
#             'previous_address': forms.TextInput(attrs={'class': 'form-control'}),
#             'highest_educational_attainment': forms.Select(attrs={'class': 'form-control'}),
#             'occupation': forms.TextInput(attrs={'class': 'form-control'}),
#             'registration_date': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
#             'block_number': forms.NumberInput(attrs={'class': 'form-control'}),
#             'house_number': forms.NumberInput(attrs={'class': 'form-control'}),
#             'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data.get('email')

#         # Check if email already exists
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError('This email is already taken.')

#         return cleaned_data
    
class HomeOwnerForm(forms.ModelForm):
    class Meta:
        model = HomeOwner
        fields = ['date_of_birth', 'age', 'contact_number', 'gender', 'relationship_to_household', 'occupation','profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50', 'type':'date', 'require': True}),
            'age': forms.NumberInput(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50', 'require': True }),
            'contact_number': forms.NumberInput(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50', 'require': True}),
            'gender': forms.Select(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50', 'require': True}),
            'relationship_to_household': forms.Select(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50', 'require': True}),
            'occupation': forms.TextInput(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50', 'require': True}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already taken.')

        return cleaned_data

class OwnerLoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password',
    }))

    def add_error(self, field, error):
        if field:
            super().add_error(field, error)
        else:
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class([error])

class SecretaryLoginForm(forms.Form):
    user_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password',
    }))