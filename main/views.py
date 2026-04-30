from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import Product, Category, CartItem, Newsletter, Review


def get_base_context(page):
    return {
        'page': page,
        'shop_name': 'Marlia',
        'categories': Category.objects.all(),
    }


def home(request):
    context = get_base_context('home')
    context['products'] = Product.objects.all()[:6]
    return render(request, 'main/home.html', context)


def products(request):
    context = get_base_context('products')
    selected_category = request.GET.get('category')
    if selected_category:
        context['products'] = Product.objects.filter(category__id=selected_category)
    else:
        context['products'] = Product.objects.all()
    context['selected_category'] = selected_category
    return render(request, 'main/products.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    avg_rating = product.average_rating()
    context = get_base_context('products')
    context['product'] = product
    context['reviews'] = reviews
    context['avg_rating'] = avg_rating
    return render(request, 'main/product_detail.html', context)


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    context = get_base_context('products')
    context['category'] = category
    context['products'] = products
    return render(request, 'main/category_detail.html', context)


def about(request):
    context = get_base_context('about')
    return render(request, 'main/about.html', context)


def contact(request):
    context = get_base_context('contact')
    return render(request, 'main/contact.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    context = get_base_context('login')
    context['form'] = form
    return render(request, 'main/auth.html', context)


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    context = get_base_context('register')
    context['form'] = form
    return render(request, 'main/auth.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)
    context = get_base_context('cart')
    context['items'] = items
    context['total'] = total
    return render(request, 'main/cart.html', context)


def cart_add(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f'"{product.name}" додано до кошика!')
    return redirect(request.META.get('HTTP_REFERER', 'products'))


def cart_remove(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')


def newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            Newsletter.objects.get_or_create(email=email)
            messages.success(request, 'Ви успішно підписались на розсилку!')
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def add_review(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        author = request.user.username
        text = request.POST.get('text')
        rating = request.POST.get('rating')
        if text and rating:
            Review.objects.create(
                product=product,
                author=author,
                text=text,
                rating=int(rating)
            )
            messages.success(request, 'Ваш відгук додано!')
    return redirect('product_detail', product_id=product_id)