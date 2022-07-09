from django import forms
class libform(forms.Form):
    Book_name = forms.CharField(max_length=30)
    Book_author = forms.CharField(max_length=30)
    Book_category = forms.CharField(max_length=30)
    #Book_number = forms.AutoField(auto_created=True, primary_key=True, editable=False, blank=True)
    Book_shelf = forms.CharField(max_length=30)
    Number_of_available_copies = forms.IntegerField()
    #Date_added = forms.DateTimeField()

class Sform(forms.Form):
    Book_name = forms.CharField(max_length=30)




