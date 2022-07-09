from django.shortcuts import render,redirect
from .models import lib, borrowed_books
from .forms import libform, Sform
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import F
from datetime import date,timedelta,time
# Create your views here.
#@authenticated_user
@user_passes_test(lambda u: u.is_staff)
def database(request):
    title = 'Book Registration'
    form = libform(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['Book_name']
        author = form.cleaned_data['Book_author']
        category = form.cleaned_data['Book_category']
        shelf_number = form.cleaned_data['Book_shelf']
        available = form.cleaned_data['Number_of_available_copies']
        p = lib(Book_name=name, Book_author=author, Book_category=category, Book_shelf=shelf_number, Number_of_available_copies=available )
        p.save()
        return render(request, 'reg.html')
    context = {
        'title':title,
        'form':form
    }
    return render(request, 'button.html',context)
@user_passes_test(lambda u: u.is_student)
def existing(request):
    title = 'List of available books'
    queryset = lib.objects.all()
    context = {
        'title':title,
        'queryset':queryset
    }
    return render(request, 'table.html', context)
def books(request):
    title = 'List of available books'
    queryset = lib.objects.all()
    context = {
        'title': title,
        'queryset': queryset
    }
    return render(request, 'books.html', context)
def search(request):
    title = 'Search for books'
    form = Sform(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['Book_name']
        queryset = lib.objects.filter( Book_name=name).values()
        contexts ={
            'title':title,
            'form': queryset,
        }
        return render(request, 'table.html', contexts)
    context = {
        'title': title,
        'form': form,

    }
    return render(request, 'search.html', context)

def home(request):
    return render(request, 'temp.html')
@user_passes_test(lambda u: u.is_staff)
def existings(request):
    title = 'List of available books'
    queryset = lib.objects.all()
    context = {
        'title':title,
        'queryset':queryset
    }
    return render(request, 'testing.html', context)
@user_passes_test(lambda u: u.is_staff)
def delete(request):
    title = 'Search for books to delete'
    form = Sform(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['Book_name']
        queryset = lib.objects.filter(Book_name=name).delete()
        return render(request, 'remove.html', {'title': 'Book details removed successfully'})

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'success.html', context)
@user_passes_test(lambda u: u.is_student)
def borrow(request):
    title = 'Search for books to borrow'
    form = Sform(request.POST or None)
    if form.is_valid():
        names = form.cleaned_data['Book_name']
        '''n = User.first_name
        f= User.last_name'''
        n=lib.Book_name
        g = lib.Date_added
        w= borrowed_books(borrower_name=names, date=g)
        w.save()
        if form.is_valid():
            name = form.cleaned_data['Book_name']
            if F('Number_of_available_copies_gte=0'):
                 lib.objects.filter(Book_name=name).update(Number_of_available_copies=F('Number_of_available_copies') - 1)
                 return render(request, 'remove.html', {'title': 'Book details removed successfully'})
        else:
            return render(request,'un.html')
    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'borrow.html',context)
@user_passes_test(lambda u: u.is_staff)
def borrowed(request):
    title = 'List of available books'
    queryset = borrowed_books.objects.all()
    context = {
        'title': title,
        'queryset': queryset
    }
    return render(request, 'borrowtable.html', context)

