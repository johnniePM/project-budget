from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields

class SignupForm(UserCreationForm):
    first_name= forms.CharField(max_length=150, help_text="Requiered. 150 characters of fewer", label="First Name")
    last_name= forms.CharField(max_length=150, help_text="Requiered. 150 characters of fewer", label="Last Name")
    email=forms.CharField(max_length=250 ,help_text="Requiered. A valid email adress", widget=forms.EmailInput(attrs={"title" : "Email Adress"}))

    class Meta:
        model = User
        fields = ["username", "email" ,"first_name",
                  "last_name", "password1", "password2"]

    def clean_email(self):
        email=self.cleaned_data.get("email")
        existing_user = User.objects.filter(email__iexact = email)
        if existing_user.exists():
            raise forms.ValidationError("A user with this email already exist")
        return email
    def clean_username(self):
        username=self.cleaned_data.get("username")
        existing_user = User.objects.filter(username__iexact = username)
        if existing_user.exists():
            raise forms.ValidationError("A user with this username already exist")
        return username