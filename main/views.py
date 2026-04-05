from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'main/home.html', {
        'categories': categories,
        'products': products
    })


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    return render(request, 'main/category_detail.html', {
        'category': category,
        'products': products
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'main/product_detail.html', {
        'product': product
    })