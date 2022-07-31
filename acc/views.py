from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib import messages

# Create your views here.
def update(request):
    if request.method == "POST":
        u = request.user
        uc = request.POST.get("ucomm")
        ue = request.POST.get("umail")
        uf = request.POST.get("fname")
        ul = request.POST.get("lname")
        pi = request.FILES.get("upic")
        if pi:
            u.pic.delete()
            u.pic = pi
        u.comment, u.email, u.first_name, u.last_name = uc, ue, uf, ul
        u.save()
        return redirect("acc:profile")

    return render(request, "acc/update.html")

def chpass(request):
    u = request.user
    cp = request.POST.get("cpass")
    if check_password(cp, u.password):
        np = request.POST.get("npass")
        u.set_password(np)
        u.save()
        return redirect("acc:login")
    return redirect("acc:update")


def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        uc = request.POST.get("ucomm")
        ue = request.POST.get("umail")
        uf = request.POST.get("fname")
        ul = request.POST.get("lname")
        pi = request.FILES.get("upic")
        try:
            User.objects.create_user(username=un, password=up, comment=uc, email=ue,
                                    first_name=uf, last_name=ul, pic=pi)
            return redirect("acc:login")
        except:
            messages.info(request, "USERNAME 이 중복되어 계정이 생성되지 않았습니다")
    return render(request, "acc/signup.html")

def delete(request):
    u = request.user
    cp = request.POST.get("cpass")
    if check_password(cp, u.password):
        u.pic.delete()
        u.delete()
        return redirect("acc:index")
    else:
        messages.error(request, "인증정보가 일치하지 않아 계정이 삭제되지 않았습니다")
    return redirect("acc:profile")

def profile(request):
    return render(request, "acc/profile.html")

def userlogout(request):
    logout(request)
    return redirect("acc:index")


def userlogin(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        u = authenticate(username=un, password=up)
        if u:
            login(request, u)
            messages.success(request, f"{un} 님 환영합니다!")
            return redirect("acc:index")
        else:
            messages.error(request, "계정정보가 일치하지 않습니다")
    return render(request, "acc/login.html")

def index(request):
    return render(request, "acc/index.html")