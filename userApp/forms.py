from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Userprofile

class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",

        ]

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = Userprofile
        fields = [
            "gender",
            "passport",
            "country",
            "state",
            "bio",
            "phone",

        ]

class AdminProfileForm(forms.ModelForm):

    class Meta:
        model = Userprofile
        fields = [
            "gender",
            "passport",
            "country",
            "state",
            "bio",
            "phone",
            "role",

        ]
