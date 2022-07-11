from django.urls import path
from . import views
urlpatterns =[
    path('register/', views.database),
    path('database/', views.existing),
    path('librarain/database/', views.existings),
    path('search/', views.search),
    path('', views.home, name='home'),
    path('remove/', views.delete),
    path('borrow/', views.borrow),
    path('borrowed/', views.borrowed),
    path('books/', views.books),
    path('return/', views.returns)

]