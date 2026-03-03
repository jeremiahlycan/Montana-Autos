from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    CATEGORY_CHOICES = [
        ("lexus", "Lexus"),
        ("mercedes_benz", "Mercedes Benz"),
        ("rolls_royce", "Rolls Royce"),
        ("bmw", "BMW"),
        ("bentley", "Bentley"),
        ("unknown", "Unknown")
    
    ]
    title = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES, default="unknown")
    # image = models.ImageField(upload_to='product_images/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ProductFeatures(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="features")
    label = models.CharField(max_length=20)
    value = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} feat-0{self.pk}"

class ProductReview(models.Model):
    RATING_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    ]

    message = models.CharField(max_length=225)
    ratings = models.PositiveIntegerField(choices=RATING_CHOICES, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    created_at = models. DateTimeField(auto_now_add=True)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.title} image-0{self.pk}"
    

