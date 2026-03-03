from django.db import models
from django.contrib.auth.models import User
from .utils import getCountries
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Userprofile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female',  "Female")
    ]
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices= GENDER_CHOICES)
    passport = models.ImageField(upload_to='passports/', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    country = models.CharField(max_length=36, choices=getCountries())
    bio = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Userprofile.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        instance.userprofile.save()




