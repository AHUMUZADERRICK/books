from django.shortcuts import render
from .models import lib
from .forms import libform, Sform


# Create your views here.
def database(request):
    title = 'Book Registration'
    form = libform(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['Book_name']
        author = form.cleaned_data['Book_author']
        category = form.cleaned_data['Book_category']
        number = form.cleaned_data['Book_number']
        shelf_number = form.cleaned_data['Book_shelf']
        p = lib(Book_name=name, Book_author=author, Book_category=category, Book_number=number, Book_shelf=shelf_number)
        p.save()
        return render(request, 'reg.html')
    context = {
        'title':title,
        'form':form
    }
    return render(request, 'button.html',context)
def existing(request):
    title = 'List of available books'
    queryset = lib.objects.all()
    context = {
        'title':title,
        'queryset':queryset
    }
    return render(request, 'table.html', context)
def search(request):
    title = 'Search for books'
    form = Sform(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['Book_name']
        queryset=lib.objects.filter(Book_name =name)
        context ={
            'title':title,
            'form': queryset
        }
        return render(request, 'table.html', context)
    context = {
        'title': title,
        'form': form,

    }
    return render(request, 'search.html', context)






