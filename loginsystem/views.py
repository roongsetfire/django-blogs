from tabnanny import check
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User,auth

from writerpanel.views import panel

# Create your views here.
def index(request):
    checkLogin = True
    return render(request,'backend/login_register.html',{'checkLogin':checkLogin})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']
        checkLogin = False

        if username == '' or email == '' or password == '' or repassword == '':
            messages.info(request,'please enter all the field')
            return render(request,'backend/login_register.html',{'checkLogin':checkLogin})
        else:
            if password == repassword:
                if User.objects.filter(username=username).exists():
                    messages.info(request,'Username is already in use')
                    return render(request,'backend/login_register.html',{'checkLogin':checkLogin})
                elif User.objects.filter(email=email).exists():
                    messages.info(request,'email is already in use')
                    return render(request,'backend/login_register.html',{'checkLogin':checkLogin})

                else:
                    user = User.objects.create_user(username=username,email=email,password=password)
                    user.save()
                    messages.info(request,'Register successful')
                    checkLogin = True
                    return render(request,'backend/login_register.html',{'checkLogin':checkLogin})
            else:
                messages.info(request,'password do not match. Please try again')
                return render(request,'backend/login_register.html',{'checkLogin':checkLogin})

def login(request):
    username = request.POST['username']
    password = request.POST['password']

    user = auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request,user)
        return redirect('panel')
    else:
        messages.info(request,'User is not register')
        return redirect('member')

def logout(request):
    auth.logout(request)
    return redirect('member')