from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .forms import SignupForm, UserForm, UserProfileForm, AdminProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Userprofile
from django.contrib import messages

# Create your views here.

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("login")
@login_required
def profileView(request, id):
    profile = get_object_or_404(Userprofile, user_id=id)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def editProfile(request, id):
    profile = get_object_or_404(Userprofile, user_id=id)
    user = profile.user

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'profile edited')
            return redirect('profile', user.id)
        
        else:
            print(user_form.errors)
            print(profile_form.errors)
            messages.errors(request, 'An error justr occured' )

    else:
        user_form = UserForm(instance=user)
        if request.user.is_superuser:
            profile_form = AdminProfileForm(instance=profile)
        else:
            profile_form = UserProfileForm(instance=profile)
            
        return render(request, 'edit_profile.html',{'user_form': user_form, 'profile_form': profile_form})