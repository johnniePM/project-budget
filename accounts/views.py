from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import authenticate, login
from .forms import SignupForm 
import datetime
date = datetime.date.today
class RegisterView(View):
    
    form=SignupForm
    def get(self,request):

        context = {
            "form"  : self.form(),
        }
        return  render(request,"accounts/signup.html",context)
    
    def post(self,request):
        form=self.form(request.POST)
        if form.is_valid():
            account=form.save()
            
            accountname = form.cleaned_data.get("accountname")
            password= form.cleaned_data.get("password1")
            account = authenticate(accountname=accountname, password=password)

        if account:
            login(request,account)
            return redirect("home:home")

        return  render(request,"accounts/register.html",{"form":form})
# Create your views here.
