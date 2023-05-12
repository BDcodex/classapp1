from django.shortcuts import render, redirect
from django.http import HttpResponse
from classecb import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User, auth
from django.contrib import messages
import urllib
from django.contrib.auth.hashers import check_password


def home(request):
    return render(request, "index.html")


def signup(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        email = request.POST.get('email')

        if pass1 == pass2:
            if User.objects.filter(username=username):
                messages.error(request, "Username already exists")
                print("username already exists")
                return redirect('signup')

            elif User.objects.filter(email=email):
                messages.error(request, "Email already exists")
                print("Email already exists")
                return redirect('signup')

            else:
                user = User.objects.create_user(username=username, password=pass1, email=email, first_name=fname, last_name=lname)

                user.save()
                print("user created")
                print("first name: ", fname)
                print("last name: ", lname)
                print("password1: ", pass1)
                print("password2: ", pass2)

                email_from = settings.EMAIL_HOST_USER
                subject = "Welcome to ECB21'25 app"
                message = "hi {} thank you for visiting our site. Please supprt and share".format(fname)
                recipient_list = [email]
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)
                messages.success(request, "Email is been sent to {}".format(email))
                return redirect(home) 

        else:
            print("passwords not matching")
            messages.error(request, "passwords not matching")
            return redirect('signup')
              

    return render(request, "signup.html")                     




def signin(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usname = User.objects.get(username = username)
            success = usname.check_password(password)
            if success:
                user=auth.authenticate(username = username, password = password)   
                # context={
                #     'welcome':"Hello",
                #     "usern" : "derin"
                # }
                if user is not None:#these are not neccessary with above code
                    auth.login(request, user)
                    messages.success(request, "Successfully Logged in")
                    return redirect('home')
                else:
                    messages.error(request, "Create an Account") 
                    return redirect('signup')  
            else:
                messages.error(request, "Incorrect Password")
                return redirect('signin')   

        except:
            messages.error(request, "Create an account")
            return redirect('signup')    


    return render(request, "signin.html")


def logout_view(request):
    auth.logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')


