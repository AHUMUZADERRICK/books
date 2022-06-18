from django.db import models

# Create your models here.
class lib(models.Model):
    Book_name = models.CharField(max_length=30)
    Book_author = models.CharField(max_length=30)
    Book_category = models.CharField(max_length=30)
    Book_number = models.CharField(max_length=30)
    Book_shelf = models.CharField(max_length=30)

