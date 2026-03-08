from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as django_messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from productApp.models import Product
from userApp.utils import getCountries
from decouple import config
import requests
import json

def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    key = str(product_id)

    if key in cart:
        if cart[key]['quantity'] < product.quantity:
            cart[key]['quantity'] += 1
        else:
            django_messages.warning(request, f'Sorry, only {product.quantity} unit(s) of {product.title} available.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
    else:
        if product.quantity == 0:
            django_messages.warning(request, f'Sorry, {product.title} is out of stock.')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        cart[key] = {
            'id': product.id,
            'title': product.title,
            'price': float(product.price),
            'quantity': 1,
            'stock': product.quantity,
            'image': product.images.first().image.url if product.images.exists() else '',
        }

    save_cart(request, cart)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def remove_from_cart(request, product_id):
    cart = get_cart(request)
    key = str(product_id)
    if key in cart:
        del cart[key]
    save_cart(request, cart)
    return redirect('cart')

def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_cart(request)
    key = str(product_id)
    quantity = int(request.POST.get('quantity', 1))

    if key in cart:
        if quantity <= 0:
            del cart[key]
            django_messages.success(request, f'{product.title} removed from cart.')
        elif quantity > product.quantity:
            cart[key]['quantity'] = product.quantity
            django_messages.warning(request, f'Only {product.quantity} unit(s) of {product.title} available. Quantity has been capped.')
        else:
            cart[key]['quantity'] = quantity
            django_messages.success(request, 'Quantity updated successfully.')

    save_cart(request, cart)
    return redirect('cart')

def view_cart(request):
    cart = get_cart(request)
    items = list(cart.values())
    total = sum(item['price'] * item['quantity'] for item in items)
    return render(request, 'cart.html', {
        'cart_items': items,
        'total': total,
        'cart_count': sum(item['quantity'] for item in items)
    })

def checkout(request):
    cart = get_cart(request)
    items = list(cart.values())
    total = sum(item['price'] * item['quantity'] for item in items)

    if not items:
        return redirect('cart')

    countries = getCountries()

    return render(request, 'checkout.html', {
        'cart_items': items,
        'total': total,
        'countries': countries,
        'PAYSTACK_PUBLIC_KEY': config('PAYSTACK_PUBLIC_KEY', default=''),
        'FLUTTERWAVE_PUBLIC_KEY': config('FLUTTERWAVE_PUBLIC_KEY', default=''),
        'STRIPE_PUBLIC_KEY': config('STRIPE_PUBLIC_KEY', default=''),
    })

def get_states(request, country_code):
    try:
        url = "https://country-state-city-search-rest-api.p.rapidapi.com/states-by-countrycode"
        headers = {
            "x-rapidapi-key": "d5c5fe5c5dmshf006ed9f1ab63d6p1c8a6djsn1caa7867a7e8",
            "x-rapidapi-host": "country-state-city-search-rest-api.p.rapidapi.com"
        }
        params = {"countrycode": country_code}
        response = requests.get(url, headers=headers, params=params)
        states = response.json()
        return JsonResponse({"states": states})
    except Exception as e:
        print(e)
        return JsonResponse({"states": []})

def verify_payment(request):
    reference = request.GET.get('reference')

    if not reference:
        django_messages.error(request, 'Payment reference missing.')
        return redirect('checkout')

    # Verify with Paystack
    try:
        headers = {
            "Authorization": f"Bearer {config('PAYSTACK_SECRET_KEY', default='')}",
            "Content-Type": "application/json"
        }
        response = requests.get(
            f"https://api.paystack.co/transaction/verify/{reference}",
            headers=headers
        )
        result = response.json()

        if result['status'] and result['data']['status'] == 'success':
            # Payment verified — reduce stock and clear cart
            cart = get_cart(request)
            for key, item in cart.items():
                try:
                    product = Product.objects.get(id=item['id'])
                    product.quantity = max(0, product.quantity - item['quantity'])
                    product.save()
                except Product.DoesNotExist:
                    pass

            clear_cart(request)
            django_messages.success(request, '🎉 Payment successful! Your order has been placed.')
            return redirect('payment-success')

        else:
            django_messages.error(request, 'Payment verification failed. Please contact support.')
            return redirect('checkout')

    except Exception as e:
        print(e)
        django_messages.error(request, 'An error occurred while verifying payment.')
        return redirect('checkout')

def payment_success(request):
    return render(request, 'payment_success.html')

def clear_cart_view(request):
    clear_cart(request)
    django_messages.success(request, 'Cart cleared successfully.')
    return redirect('cart')
