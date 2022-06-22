from django import forms
class libform(forms.Form):
    Book_name = forms.CharField(max_length=30)
    Book_author = forms.CharField(max_length=30)
    Book_category = forms.CharField(max_length=30)
    Book_number = forms.CharField(max_length=30)
    Book_shelf = forms.CharField(max_length=30)
class Sform(forms.Form):
    Book_name = forms.CharField(max_length=30)


