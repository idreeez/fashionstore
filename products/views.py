from django.shortcuts import render
from .models import Product, Category

def product_list(request):
    categories = Category.objects.all()
    category_products = {
        category: Product.objects.filter(category=category, available=True)
        for category in categories
    }
    return render(request, 'products/list.html', {
        'category_products': category_products
    })
