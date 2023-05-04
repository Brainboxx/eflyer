from django.shortcuts import render
from core.models import Cart

# Create your views here.
def payment(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    items = []
    total_cost = 0
    for cart_item in cart_items:
        item_price = cart_item.item.price
        item_quantity = int(cart_item.quantity)
        total_price = item_price * item_quantity
        item = {
            'name': cart_item.item.name,
            'quantity': item_quantity,
            'price': item_price,
            'total_price': total_price,
        }
        items.append(item)
        total_cost += total_price

    context = {
        'items': items,
        "total_cost": total_cost
    }
    return render(request, 'payment/payment.html', context)
