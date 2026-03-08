
"""
URL configuration for ojaoba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from productApp import views
from django.conf import settings
from django.conf.urls.static import static
from userApp.views import SignupView, profileView, editProfile, toggleWishlist, wishlistPage, removeWishlist
 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cartApp.urls")),
    path("", views.getHome, name="home"),
    path("cars/", views.getProducts, name="cars"),
    path("get-cars/<int:product_id>/", views.getproductbyId, name="get-cars"),
    path("add-cars/", views.addproduct, name="add-cars"),
    path("add-image/<int:product_id>/", views.addImage, name="add-image"),
    path("add-feature/<int:product_id>/", views.addFeature, name="add-feature"),
    path("edit-post/<int:product_id>/", views.editProduct, name="edit-post"),
    path("delete-post/<int:product_id>/", views.deleteProduct, name="delete-post"),
    path("edit-image/<int:image_id>/", views.editImage, name="edit-image"),
    path("delete-image/<int:image_id>/", views.deleteImage, name="delete-image"),
    path("edit-feature/<int:feature_id>/", views.editFeature, name="edit-feature"),
    path("delete-feature/<int:feature_id>/", views.deleteFeature, name="delete-feature"),
    path("dashboard/", views.dealerDashboard, name="dealer-dashboard"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("membership/signup", SignupView.as_view(), name="signup"),
    path("profile/<int:id>/", profileView, name="profile"),
    path("edit-profile/<int:id>/", editProfile, name="edit-profile"),
    path("brands/", views.brands, name="brands"),
    path("brands/<str:category>/", views.brandProducts, name="brand-products"),
    path('wishlist/', wishlistPage, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', toggleWishlist, name='toggle-wishlist'),
    path('wishlist/remove/<int:product_id>/', removeWishlist, name='remove-wishlist'),
        


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)