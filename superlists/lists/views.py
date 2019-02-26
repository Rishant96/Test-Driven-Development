from django.shortcuts import redirect, render

from lists.models import Item


def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_next'])
        return redirect('/')

    return render(request, 'lists/home.html')
