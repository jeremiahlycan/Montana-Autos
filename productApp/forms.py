from django import forms
from .models import Product, ProductImage, ProductFeatures

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            "title",
            "quantity",
            "price",
            "description",
            "category",
        ]

class ImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = [
            'image'
        ]

class FeatureForm(forms.ModelForm):
    class Meta:
        model = ProductFeatures
        fields = [
            'label',
            'value'
        ]

