from polls.models import Question
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context





# Create your views here.


def home(request):
    return render(request, 'pages/home.html')

def landing(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'pages/landing.html', context)

def user_login(request):
    print('hello')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/home')
        else:
            messages.info(request,'Invalid username or password')
            return redirect('login')
    else:
        return render(request,'userreg/login.html')

def user_logout(request):
    logout(request)
    messages.success(request,("You Were Logged Out!"))
    return redirect('/')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        hashed_password = make_password(password)
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            messages.info(request,'Already have an account with same email id')
            return redirect(user_signup)
        else:
            user = User(username=username,password=hashed_password,email=email)
            user.save()
            user = authenticate(request, username=username, password=password)
            login(request,user)
            return redirect('/home')
    return render(request,'userreg/signup.html')