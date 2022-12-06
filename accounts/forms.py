from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegisterForm(forms.ModelForm):
    password2 = forms.CharField(required=True, min_length=8, max_length=20, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        widgets = {
            'password': forms.PasswordInput
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('this username is already in use')
        if username == 'admin':
            raise ValidationError('you can not use this username')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        user_email = User.objects.filter(email=email).exists()
        if user_email:
            raise ValidationError('this email is already in use')
        return email

    def clean(self):
        cd = super().clean()
        password1 = cd.get("password")
        password2 = cd.get("password2")
        if password1 and password2 and password2 != password1:
            raise ValidationError('passwords are not match')


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
