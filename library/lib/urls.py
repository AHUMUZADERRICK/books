from django.urls import path
from . import views
urlpatterns =[
    path('register/', views.database),
    path('database/', views.existing),
    path('librarain/database/', views.existings),
    path('search/', views.search),
    path('', views.home),
    path('remove/', views.delete),
]