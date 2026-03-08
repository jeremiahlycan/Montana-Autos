from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .forms import SignupForm, UserForm, UserProfileForm, AdminProfileForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Userprofile, Wishlist
from productApp.models import Product
from django.contrib import messages
from django.http import JsonResponse

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("login")

@login_required
def profileView(request, id):
    profile = get_object_or_404(Userprofile, user_id=id)
    wishlist = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'profile.html', {
        'profile': profile,
        'wishlist': wishlist
    })

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
            messages.success(request, 'Profile edited successfully')
            return redirect('profile', user.id)
        else:
            messages.error(request, 'An error just occurred')

    else:
        user_form = UserForm(instance=user)
        if request.user.is_superuser:
            profile_form = AdminProfileForm(instance=profile)
        else:
            profile_form = UserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def toggleWishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        # Already wishlisted — remove it
        wishlist_item.delete()
        return JsonResponse({'status': 'removed', 'message': f'{product.title} removed from wishlist'})

    return JsonResponse({'status': 'added', 'message': f'{product.title} added to wishlist ❤️'})

@login_required
def wishlistPage(request):
    wishlist = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist.html', {'wishlist': wishlist})

@login_required
def removeWishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f'{product.title} removed from wishlist.')
    return redirect('wishlist')