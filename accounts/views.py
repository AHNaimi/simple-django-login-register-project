from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as authen_view
from django.urls import reverse_lazy


class UserRegisterView(View):
    form = UserRegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form1 = self.form
        return render(request, 'accounts/register.html', {"form": form1})

    def post(self, request):
        form1 = self.form(request.POST)
        if form1.is_valid():
            valid_form = form1.cleaned_data
            user = User.objects.create_user(valid_form['username'], valid_form['email'], valid_form['password'])
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'you registered successfully')
            return redirect('home:home')
        return render(request, 'accounts/register.html', {"form": form1})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user1 = authenticate(request, username=cd['username'], password=cd['password'])
            if user1 is not None:
                login(request, user1)
                messages.success(request, 'you logged in successfully')
                return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        messages.info(request, "you log out successfully")
        return redirect("home:home")


class UserPasswordResetView(authen_view.PasswordResetView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_success')
    email_template_name = 'accounts/password_content_reset_email.html'


class UserResetPasswordDoneView(authen_view.PasswordResetDoneView):
    template_name = 'accounts/password_reset_success.html'


class PasswordResetConfirmView(authen_view.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy('accounts:password_reset_complete')


class PasswordResetCompleteView(authen_view.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
