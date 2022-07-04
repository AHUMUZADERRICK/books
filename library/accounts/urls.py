from  django.urls import path
from .import views
urlpatterns = [
    path('register/',views.register,name='register'),
    path('student_register/', views.student_register.as_view(), name = 'student_register'),
    path('librarain_register/', views.librarain_register.as_view(), name='librarain_register'),
    path('login/', views.login_view, name='login'),
    path('librarain/', views.librarain, name='librarain'),
    path('student/', views.student, name='student'),
    path('logout/', views.logout_view, name='logout'),

]