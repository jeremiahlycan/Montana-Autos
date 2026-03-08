from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.view_cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/states/<str:country_code>/', views.get_states, name='get-states'),
    path('verify-payment/', views.verify_payment, name='verify-payment'),
    path('payment-success/', views.payment_success, name='payment-success'),
    path('cart/clear/', views.clear_cart_view, name='clear-cart'),
]