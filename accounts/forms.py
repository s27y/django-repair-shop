from django import forms
from django.forms import ModelForm
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from .models import Profile

class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'example@gmail.com','class':'form-control'}))
    password = forms.CharField(label=_("Password"), 
        widget=forms.PasswordInput(attrs={'class':'form-control'}))



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class UserCreateForm(UserCreationForm):
    #email = forms.EmailField(required=True)
    username = forms.CharField(max_length=20, min_length=4,
        widget=forms.TextInput(attrs = {'placeholder': 'Username','class':'form-control'}))
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    def isValidUsername():
        return True
    class Meta:
        model = User

        fields = ("username", "password1", "password2", "email")
        widgets = {
            'email': forms.TextInput(attrs = {'placeholder': 'E-Mail','class':'form-control '}),
        }

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(attrs = {'class':'form-control'}))
    last_name  = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(attrs = {'class':'form-control'}))
    class Meta:
        model = Profile
        fields = ['company_name','first_name', 'last_name', 'contact_number']
        widgets = {
            'company_name' : forms.TextInput(attrs = {'class':'form-control'}),
            'contact_number' : forms.TextInput(attrs = {'class':'form-control'}),
        }
