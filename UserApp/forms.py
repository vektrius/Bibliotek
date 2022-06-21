from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from UserApp.models import Account


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'user name'}))
    password = forms.CharField(min_length=6, max_length=32,
                               widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    confirm_password = forms.CharField(min_length=6, max_length=32,
                                       widget=forms.PasswordInput(attrs={'placeholder': 'password confirm'}))
    email = forms.CharField(max_length=60, widget=forms.EmailInput(attrs={'placeholder': 'email'}))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'user name'}))
    password = forms.CharField(min_length=6, max_length=32,
                               widget=forms.PasswordInput(attrs={'placeholder': 'password'}))

    # Попробовать засунуть всё это в def clean
    def clean(self):
        user = User.objects.filter(username=self.cleaned_data['username']).first()
        if user:
            if not authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password']):
                self.add_error('password', ValidationError('Неверный пароль!'))
        else:
            self.add_error('username', ValidationError('Неверный логин!'))
        super(LoginForm, self).clean()


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['age', 'sex', 'region', 'likes_genre', 'about_me']

        widgets = {
            'about_me': forms.Textarea(attrs={}),
        }
    name = forms.CharField(max_length=50, label='Name')

