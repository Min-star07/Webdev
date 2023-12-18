from django.shortcuts import render,redirect
from django import forms
from django.shortcuts import render, HttpResponse
from utils.encrypt import md5
from web import models

class LoginForm(forms.Form):
    username = forms.CharField(label ="Username", widget=forms.TextInput(
        attrs={"class":"form-control", "placeholder":"Enter your username or email"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={"class": "form-control", "placeholder": "Enter your password"}, render_value=True) )

# Create your views here.
def index(request):
    # return HttpResponse("welcom django")
    return render(request, "web/index.html")

def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'web/login.html', {"form": form})
    form = LoginForm(data = request.POST)
    if not form.is_valid():
        return render(request, 'web/login.html', {"form": form})
    #验证码正确，去数据库验证用户和密码
    user = form.cleaned_data["username"]
    pwd = form.cleaned_data["password"]
    print(user, pwd)                                                                                                                        
    user_object = models.User.objects.filter(username=user, password =pwd).first()
    if not user_object:
        # form.add_error("password", "invalid user or password")
        return render(request, 'web/login.html', {"form": form, "error": "invalid user or password"})
    # request.session["info"] = { " name":user_object.username}
    # request.session.set_expiry(60*60*24*7)                                                            
    return redirect('/index/')