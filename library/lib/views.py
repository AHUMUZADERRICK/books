import datetime
from django.shortcuts import render,redirect
from .models import lib, borrowed_books
from .forms import libform, Sform
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import F
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
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
        p = lib(Book_name=name, Book_author=author, Book_category=category, Book_shelf=shelf_number, Number_of_available_copies=available)
        p.save()
        messages.success(request, 'Book is registered successfully')
        return redirect('/register/')
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
        queryset = lib.objects.get( Book_name=name)
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
def borrow(request, Book_number):
      try:
          book = lib.objects.get(Book_number=Book_number)
          lib.objects.filter(Book_number=Book_number).update(Number_of_available_copies=F('Number_of_available_copies') - 1)
      except IntegrityError:
          messages.success(request, 'Book is out of stock')
          return redirect('/database/')
      x = request.user.first_name
      y = request.user.last_name
      z = request.user.Reg
      N = request.user.books_borrowed
      g = datetime.datetime.now()
      return_date = datetime.datetime.now() + datetime.timedelta(weeks=1)
      w = borrowed_books(book_title=book.Book_name, borrower_fname=x, date=g, borrower_lname=y, borrower_number=z,
                         Return=return_date, book_number= Book_number,fine=N)
      w.save()
      messages.success(request, 'Book is borrowed successfully and your return ID is in your borrowed books folder')
      return redirect('/database/')

@user_passes_test(lambda u: u.is_staff)
def borrowed(request):
    title = 'List of borrowed books'
    queryset = borrowed_books.objects.all()
    context = {
        'title': title,
        'queryset': queryset
    }
    return render(request, 'borrowtable.html', context)
@user_passes_test(lambda u: u.is_staff)
def returns(request,q):
    b = borrowed_books.objects.get(q=q)
    lib.objects.update(Number_of_available_copies=F('Number_of_available_copies')+1)
    borrowed_books.objects.filter(q=b.q).delete()
    messages.success(request, 'Book returned successfully')
    return redirect('/borrowed/')

@user_passes_test(lambda u: u.is_staff)
def check_return(request):
    title = 'Search for books to return'
    form = Sform(request.POST or None)
    try:
        if form.is_valid():
            name = form.cleaned_data['Book_name']
            queryset = borrowed_books.objects.get(q=name)
            contexts = {
                'title': title,
                'form': queryset,
            }
            return render(request, 'borrowtable.html', contexts)
    except AttributeError:
        messages.success(request, 'Return code invalid')
        return redirect('/return/')
    except ValueError:
        messages.success(request, 'Return code invalid')
        return redirect('/return/')
    except TypeError:
        messages.success(request, 'Return code invalid')
        return redirect('/return/')
    except ObjectDoesNotExist:
        messages.success(request, 'Return code invalid')
        return redirect('/return/')
    context = {
            'title': title,
            'form': form,
        }
    return render(request, 'search.html', context)

