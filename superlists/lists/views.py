from django.shortcuts import redirect, render

from lists.models import Item


def home_page(request):
    if request.method == 'POST':
        print('POST')
        Item.objects.create(text=request.POST['item_next'])
        return redirect('/lists/the-only-list-in-the-world')

    items = Item.objects.all()
    return render(request, 'lists/home.html', {'items': items})


def view_list(request):
    items = Item.objects.all()
    return render(request, 'lists/home.html', {'items': items})
