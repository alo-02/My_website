from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class UserRegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)
    phone = forms.CharField(required=False)
    gender = forms.ChoiceField(
        required=False,
        choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))
    )
    qualification = forms.CharField(required=False)
    expertise = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password1', 'password2',
            'role', 'phone', 'gender', 'qualification', 'expertise',
            'profile_photo',
        ]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'email', 'phone', 'gender', 'qualification',
            'expertise', 'profile_photo',
        ]
