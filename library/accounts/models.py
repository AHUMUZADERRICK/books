from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    WebMail = models.EmailField(default=True, unique=True)
    Reg = models.CharField(max_length=100,default=True,unique=True,null=False)
    books_borrowed = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.books_borrowed = self.books_borrowed + 1
        super().save(*args, **kwargs)
    def __str__(self):
        return self.email

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=True)

class librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=True)



