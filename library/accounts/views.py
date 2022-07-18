from django.shortcuts import render, redirect
from django.views.generic import CreateView
from .forms import StudentSignUpForm,librarainSignUpForm
from .models import User,librarian,Student
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from .decorators import unauthenticated_user,authenticated_user,set
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from .utils import generate_token
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings
# Create your views here.
def send_action_email(request,user):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('../templates/activate.html',{
        'user': user,
        'domain': current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.Reg)),
        'token': generate_token.make_token(user),
    })
    email=EmailMessage(subject=email_subject,body=email_body,from_email=settings.EMAIL_FROM_USER,to=[user.WebMail])
    email.send()
def register(request):
    return render(request, '../templates/registeruser.html')

@user_passes_test(lambda u: u.is_staff)
def librarain(request):
    return render(request, '../templates/librarain.html' )

@user_passes_test(lambda u: u.is_student)
def student(request):
    return render(request, '../templates/student.html' )

class student_register(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = '../templates/studform.html'

    #@user_passes_test(lambda u: u.is_superuser)
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/accounts/login/')

class librarain_register(CreateView):
    model = User
    form_class = librarainSignUpForm
    template_name = '../templates/libform.html'
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/accounts/librarain/')


def login_view(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            '''if not user.is_email_verified:
                messages.add_message(request, messages.ERROR, 'Webmail is not verified please check your webmail inbox')
                return redirect('/accounts/login/' )'''
            if user is not None:
               if user.is_staff:
                    login(request, user)
                    return redirect('/accounts/librarain/')
               else:
                   login(request, user )
                   return redirect(('/accounts/student/'))
        else:
                messages.success(request, 'Invalid username or password')
                return render(request, '../templates/login.html')
    else:
       context ={
            'form':AuthenticationForm,
            'title':'Welcome to the login Page'
         }
       return render(request, '../templates/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')
def activate_user(request, uid64, token):
    try:
        uid=force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(Reg=uid)

    except Exception as e:
        user=None
    if user and generate_token.check_token(user, token):
        User.is_email_verified=True
        User.save()

        messages.add_message(request, messages.SUCCESS, 'Email verified, you can logi')
        return redirect(reverse('login'))

    return render(request, '../templates/activatefailed.html',{'user':user} )
