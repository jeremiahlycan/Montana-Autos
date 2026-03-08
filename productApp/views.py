
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductFeatures
from .forms import ProductForm, ImageForm, FeatureForm, ProductImage
from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from .utils import is_staff_required, is_superuser_required
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.db.models import Count


# Create your views here.

products = [
        {
            "name": "2022 Lexus Rx 350",
            "price": 20000000,
            "description": "2022 Lexus RX 350",
            "image": "https://www.cnet.com/a/img/resize/c5c64025c4b3403291e7bd345dfdf5806e3322ac/hub/2019/05/29/b6d8f98e-4c18-4087-9605-ecc74c94acd6/2020-lexus-rx-350-f-sport-02.jpg?auto=webp&width=1200"
        },
        {
            "name": " 2022 Mercedes-Benz CLS 53",
            "price": 100000000,
            "description": "2022 Mercedes-Benz CLS 53 AMG",
            "image": "https://www.inghamdriven.nz/wp-content/files/stock/HAM/22346/29705_05.jpg?width=2048&optimize=medium"
        },
        {
            "name": "2024 Rolls-Royce",
            "price": 300000000,
            "description": "2024 Rolls-Royce Phantom",
            "image": "https://www.lamborghinigoldcoast.com/imagetag/11238/2/l/New-2024-Rolls-Royce-Phantom-EWB-PLATINO-COLLECTION-1723573147.jpg"
        },
        {
            "name": "2023 Bentley Bentayga",
            "price": 35000000,
            "description": "2023 Bentley BENTAYGA S V8",
            "image": "https://www.exclusiveautomotivegroup.com/imagetag/3669/main/l/New-2023-Bentley-BENTAYGA-S-V8-1693328137.jpg"
        }
    ]

def getHome(request):
    username = "IKE Montana"

    products = Product.objects.all().order_by("-created_at")
    # products = product.objects.all()
    # products = product.objects.filter(id=1)
    # products = product.objects.filter(title='pRoduct 2')
    # products = product.objects.filter(title_iexact='pRoduct 2')
    # products = product.objects.filter(title_icontains='pRo')
    # products = product.objects.filter(title_contains='pRo')
    # products = product.objects.filter(quantity_gt=10)
    # products = product.objects.get(id=1)
    # print(product.description)
    # print(products)




    return render(
        request,
        template_name="index.html",
        context={"name": username, "products": products[0:4]}
    )

def getProducts(request):
    q = request.GET.get('q', '')
    cars = (Product.objects
            .all()
            .prefetch_related("features", "images", "reviews")
            .order_by("-created_at")
            )
    if q:
        cars = cars.filter(title__icontains=q)

    return render(
        request,
        template_name="products.html",
        context={"products": cars, "query": q}
    )

def getproductbyId(request, product_id):  
    cars = get_object_or_404(Product, id=product_id)
    return render(
        request=request,
        template_name="single_product.html",
        context={"product": cars}
    )

@user_passes_test(is_superuser_required)
def addproduct(request):
    # print(request.user.email)

    if request.method == "POST":

        form = ProductForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.created_by = request.user
            form.save()
            send_mail(
                subject="New Product Alert",
                message=f"A new product has been added by {request.user.first_name} {request.user.last_name}",
                from_email=f"MLA <{settings.DEFAULT_FROM_EMAIL}>",
                recipient_list=[request.user.email],
                fail_silently=True
            )
            messages.success(request, 'Car added successfully')
        else:
            messages.error(request, 'An error just occured')

        return redirect('cars')

    else: 
        form = ProductForm()
        return render(
            request,
            template_name="product_form.html",
            context={
                "form":form,
                "title": "Product Form"
            }
        )
@user_passes_test(is_staff_required)   
def addImage(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = ImageForm (request.POST or None, request.FILES or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.save()

        return redirect("get-cars", product_id)
    else:
        form = ImageForm()
        return render(
            request,
            template_name="product_form.html",
            context={
                "form":form,
                "title": "Upload Image"
            }
        )
    
@user_passes_test(is_staff_required)
def addFeature(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        form = FeatureForm (request.POST or None, request.FILES or None)
        if form.is_valid():
            form = form.save(commit=False)
            form.product = product
            form.save()

        return redirect("get-cars", product_id)
    else:
        form = FeatureForm()
        return render(
            request,
            template_name="product_form.html",
            context={
                "form":form,
                "title": "Feature Form"
            }
        )
    
@user_passes_test(is_superuser_required)  
def editProduct(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user != product.created_by:
        return redirect("get-cars", product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product edited successdfully')
            send_mail(
                subject="Product Edited Alert",
                message=f"Product ID0{product.id} has been edited by {request.user.first_name} {request.user.last_name}",
                from_email=f"MLA <{settings.DEFAULT_FROM_EMAIL}>",
                recipient_list=[request.user.email],
                fail_silently=True
            )
        else:
            messages.error(request, 'An error occured')

        return redirect("get-cars", product_id)
    
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        template_name="product_form.html",
        context={
            "form": form,
            "title": "Edit post"
        }
    )

@user_passes_test(is_superuser_required)
def deleteProduct(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user != product.created_by:
        return redirect("get-cars", product_id)

    if request.method == "POST":
        product.delete()
        return redirect("cars")

    return render(
        request,
        template_name="delete_product.html",
        context={"product": product}
    )

@user_passes_test(is_staff_required)
def editImage(request, image_id):
    image = get_object_or_404(ProductImage, id=image_id)

    if request.user != image.product.created_by:
        return redirect("get-cars", image.product.id)

    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return redirect("get-cars", image.product.id)
    else:
        form = ImageForm(instance=image)

    return render(
        request,
        "product_form.html",
        {
            "form": form,
            "title": "Edit Image"
        }
    )

@user_passes_test(is_staff_required)
def deleteImage(request, image_id):
    image = get_object_or_404(ProductImage, id=image_id)

    if request.user != image.product.created_by:
        return redirect("get-cars", image.product.id)

    if request.method == "POST":
        image.delete()
        return redirect("get-cars", image.product.id)

    return render(
        request,
        "delete_product.html",
        {
            "title": "Delete Image",
            "object": image,
            "product": image.product
        }
    )

@user_passes_test(is_staff_required)
def editFeature(request, feature_id):
    feature = get_object_or_404(ProductFeatures, id=feature_id)

    if request.user != feature.product.created_by:
        return redirect("get-cars", product_id=feature.product.id)

    if request.method == "POST":
        form = FeatureForm(request.POST, instance=feature)
        if form.is_valid():
            form.save()
            return redirect("get-cars", product_id=feature.product.id)
    else:
        form = FeatureForm(instance=feature)

    return render(
        request,
        "product_form.html",
        {
            "form": form,
            "title": "Edit Feature"
        }
    )

@user_passes_test(is_staff_required)
def deleteFeature(request, feature_id):
    feature = get_object_or_404(ProductFeatures, id=feature_id)

    
    if request.user != feature.product.created_by:
        return redirect("get-cars", product_id=feature.product.id)

    if request.method == "POST":
        feature.delete()
        return redirect("get-cars", product_id=feature.product.id)

    return render(
        request,
        "delete_product.html",
        {
            "title": "Delete Feature",
            "object": feature,
            "product": feature.product
        }
    )

@user_passes_test(is_staff_required)
def dealerDashboard(request):
    products = Product.objects.filter(created_by=request.user)

    total_products = products.count()
    total_images = ProductImage.objects.filter(
        product__created_by=request.user
    ).count()

    context = {
        "products": products,
        "total_products": total_products,
        "total_images": total_images,
    }

    return render(
        request,
        "dealer_dashboard.html",
        context
    )

def brands(request):
    category_counts = (
        Product.objects
        .values("category")
        .annotate(total=Count("id"))
    )

    counts_dict = {
        item["category"]: item["total"]
        for item in category_counts
    }

    categories = []
    for key, label in Product.CATEGORY_CHOICES:
        categories.append({
            "key": key,
            "label": label,
            "total": counts_dict.get(key, 0)
        })

    return render(
        request,
        "brands.html",
        {
            "categories": categories
        }
    )

def brandProducts(request, category):
    valid_categories = dict(Product.CATEGORY_CHOICES)
    
    if category not in valid_categories:
        return render(
            request,
            "404.html",
            {"message": f"Brand '{category}' does not exist."},
            status=404
        )

    products = (
        Product.objects
        .filter(category=category)
        .prefetch_related("features", "images", "reviews")
        .order_by("-created_at")
    )

    category_display = valid_categories[category]

    return render(
        request,
        "products.html",
        {
            "products": products,
            "brand_name": category_display,
            "category_key": category,
            "total": products.count()
        }
    )


