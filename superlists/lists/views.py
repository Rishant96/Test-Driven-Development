from django.shortcuts import redirect, render

from lists.models import Item


def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_next'])
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'lists/home.html', {'items': items})
