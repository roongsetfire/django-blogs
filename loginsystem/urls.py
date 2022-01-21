from django.urls import path

from loginsystem.views import index, login,register,logout

urlpatterns = [
    path('member',index,name='member'),
    path('register/add',register,name='addUser'),
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
]