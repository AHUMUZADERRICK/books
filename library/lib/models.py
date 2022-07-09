from django.db import models
import datetime
from django.urls import reverse
from django.db.models import Max,F

# Create your models here.
class lib(models.Model):
    Book_name = models.CharField(max_length=30)
    Book_author = models.CharField(max_length=30)
    Book_category = models.CharField(max_length=30)
    Book_number = models.AutoField(auto_created=True,primary_key=True,editable=False,blank=True )
    Book_shelf = models.CharField(max_length=30)
    Number_of_available_copies = models.PositiveIntegerField(blank=False,null=True)
    Date_added = models.DateTimeField(auto_now_add=True, blank=True)

    def borrow(self):
        y=lib.Number_of_available_copies
        y -=1
        y.save()

class borrowed_books(models.Model):
    borrower_name = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)




