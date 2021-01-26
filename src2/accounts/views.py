from django.contrib import messages
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.views import View
from .forms import UserRegisterForm

from django.contrib.auth import logout  , login , authenticate

class Login(View):
    def get(self , request , *args , **kwargs):
        return render(request , "login.html" , {} )

class Signup(View):
    def get(self , request , *args , **kwargs):
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self , request , *args , **kwargs):

        form = UserRegisterForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('calendar')
        messages.warning(request, f'Error ! Please review the following instruction for signup  ')
        return redirect('register')


def Logout(request):
    logout(request)
    return redirect('login')
    messages.warning(request, f'Logout successfully !')