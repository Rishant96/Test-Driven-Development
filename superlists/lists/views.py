from django.shortcuts import render
from django.http import HttpResponse


def home_page(request):
    return render(request, 'lists/home.html', {
        'new_item': request.POST.get('item_next', ''),
    })
