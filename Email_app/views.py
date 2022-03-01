from cgitb import html
from cmath import e
import email
from multiprocessing import context
from django.contrib import messages
from urllib import request
import uuid
from django.conf import settings
from django.shortcuts import redirect, render
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
# Create your views here.
def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/')
        
        login(request, user)
        return redirect('/home')

    return render(request , 'login.html')

def sent_email(request):
    return render(request, 'sent_mail.html')
def signupview(request):
    if request.method== 'POST':
        username= request.POST.get('username')
        email= request.POST.get('email')
        password= request.POST.get('password')
        try:
            if User.objects.filter(username=username):
                messages.success(request, 'Username is taken')
                return redirect(request, 'signup.html')
            if User.objects.filter(email=email):
                messages.success(request, 'Email is already in use')
                return redirect(request, 'signup.html')
            

            user_obj= User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
         
            auth_token= str(uuid.uuid4())
            profile_obj= Profile.objects.create(user = user_obj, auth_token = auth_token)
            profile_obj.save() 
            context= {'user_obj': user_obj}
            sent_mail_verification(email, auth_token)
            
            return redirect('/sent_email', context)
        except Exception as e:
            print(e)
    
    return render(request, 'signup.html')

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')
def sent_mail_verification(email, token):
    subject= 'Account Verification Required'
    message= f'Hi click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from= settings.EMAIL_HOST_USER
    recipient_list= [email]
    send_mail(subject, message, email_from, recipient_list)

def home(request):
    return render(request, 'home.html')