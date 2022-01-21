from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User,auth

from writerpanel.views import panel

# Create your views here.
def index(request):
    return render(request,'backend/login_register.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']

        if username == '' or email == '' or password == '' or repassword == '':
            messages.info(request,'please enter all the field')
            return redirect('member')
        else:
            if password == repassword:
                if User.objects.filter(username=username).exists():
                    messages.info(request,'Username is already in use')
                    return redirect('member')
                elif User.objects.filter(email=email).exists():
                    messages.info(request,'email is already in use')
                    return redirect('member')

                else:
                    user = User.objects.create_user(username=username,email=email,password=password)
                    user.save()
                    messages.info(request,'Register successful')
                    return redirect('member')
            else:
                messages.info(request,'password do not match. Please try again')
                return redirect('member')

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