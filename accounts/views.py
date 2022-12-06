from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate


class UserRegisterView(View):
    form = UserRegisterForm

    def get(self, request):
        form1 = self.form
        return render(request, 'accounts/register.html', {"form": form1})

    def post(self, request):
        form1 = self.form(request.POST)
        if form1.is_valid():
            valid_form = form1.cleaned_data
            user = User.objects.create_user(valid_form['username'], valid_form['email'], valid_form['password'])
            user.save()
            login(request, user)
            messages.success(request, 'you registered successfully')
            return redirect('home:home')
        return render(request, 'accounts/register.html', {"form": form1})


class UserLoginView(View):
    form = UserLoginForm

    def get(self, request):
        form1 = self.form
        return render(request, 'accounts/login.html', {"form": form1})

    def post(self, request):
        form1 = self.form(request.POST)
        if form1.is_valid():
            cd = form1.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                messages.success(request, 'you log in successfully')
                return redirect("home:home")
        return render(request, 'accounts/login.html', {"form": form1})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home:home")
