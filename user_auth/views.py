import email
from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import List
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
# Create your views here.

def home(request):
    return render(request, 'user_auth/index.html')

def signup(request):
    if request.method == 'POST':
        #username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            message.error(request,"Username already taken please try some other username")
            return redirect("auth/signup")
        if User.objects.filter(email=email):
            message.error(request,"Email already taken please try some other email")
            return redirect("auth/signup")
        if pass1 != pass2:
            message.error(request,"Password didn't match")
        if not username.isalnum():
            message.error(request,"Username name must be alphanumeric")
            return redirect("auth/signup")
            
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        messages.success(request, "Your account has beem successfully created")

        return redirect('/auth/signin')
    return render(request, 'user_auth/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            data=List.objects.all()
            return HttpResponseRedirect('/auth/dashboard')
            #return render(request, "user_auth/index.html",{'fname': fname})
        else:
            messages.error(request, "Bad Credentials")
            return redirect("home")
    return render(request, "user_auth/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return HttpResponseRedirect('/auth/')

def page(request):
    data=List.objects.all()
    return render(request,"abc.html",{"data":data})

def dashboard(request):
    return render(request, 'user_auth/dashboard.html')
