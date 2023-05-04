from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from items.models import Item, Category
from django.db.models import Q
from django.db import IntegrityError
from .models import Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
    categories = Category.objects.all()
    items = Item.objects.order_by('-created_at')
    user = request.user
    num_of_cart_items = 0
    if user.is_authenticated:
        cart_items = Cart.objects.filter(user=user)
        num_of_cart_items += len(cart_items)

    # query = request.GET.get('query', '')
    context = {
        'categories': categories,
        'items': items,
        'num_of_cart_items': num_of_cart_items
    }
    return render(request, 'core/index.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if password == password2:
                try:
                    user = User.objects.create_user(username=username, email=email, password=password,
                                                    first_name=firstname, last_name=lastname)
                    user.save()
                    messages.success(request, 'User account was created successfully!')
                    return redirect('login')
                except IntegrityError:
                    messages.error(request, 'A user with that username already exists.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords does not match')
            return redirect('register')

    return render(request, 'core/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('login')
    else:
        return render(request, 'core/login.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
def add_to_cart(request, pk):
    if request.method == 'POST':
        user = request.user
        item = Item.objects.get(pk=pk)
        quantity = request.POST['quantity']
        cart = Cart.objects.create(user=user, item=item, quantity=quantity)
        cart.save()
        return redirect('home')
    return render(request, 'core/cart.html')

@login_required
def cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    items = []
    total_cost = 0
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if not item_id:
            messages.error(request, "Invalid item id")
            return redirect('cart')
        try:
            cart_item = Cart.objects.get(id=item_id)
            cart_item.delete()
            messages.success(request, "Item removed from cart")
            return redirect('cart')
        except Cart.DoesNotExist:
            messages.error(request, "Item does not exist in cart")
            return redirect('cart')
    for cart_item in cart_items:
        item_price = cart_item.item.price
        item_quantity = int(cart_item.quantity)
        total_price = item_price * item_quantity
        item = {
            'item_id': cart_item.id,
            'name': cart_item.item.name,
            'quantity': item_quantity,
            'price': item_price,
            'total_price': total_price,
        }
        items.append(item)
        total_cost += total_price
    context = {
        'items': items,
        'total_cost': total_cost
    }
    return render(request, 'core/cart.html', context)

def search(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.all()
    user = request.user
    num_of_cart_items = 0

    if user.is_authenticated:
        cart_items = Cart.objects.filter(user=user)
        num_of_cart_items = len(cart_items)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    context = {
        'items': items,
        'query': query,
        'category_id': int(category_id),
        'categories': categories,
        'num_of_cart_items': num_of_cart_items
    }

    return render(request, 'items/search.html', context)


