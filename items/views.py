from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, Category

# Create your views here.
def new(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        category = request.POST['category']
        category, created = Category.objects.get_or_create(name=category)
        image = request.FILES.get('image')
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']

        new_item = Item.objects.create(category=category, image=image, name=name, description=description, price=price)
        new_item.save()

        return redirect('home')
    context={
        'categories':categories
    }
    return render(request, 'items/form.html', context)

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category).exclude(pk=pk)[0:3]

    context = {
        'item': item,
        'related_items': related_items
    }
    return render(request, 'items/detail.html', context)

