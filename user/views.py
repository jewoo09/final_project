
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm, RegisterForm

User = get_user_model()


def index(request):

    user=User.objects.filter(id=request.user.id).first
    return render(request, "index.html",{"username":user})

    if request.user.is_authenticated is False:
    
        return render(request, "index.html",{"username":"로그인못함"})


    #print(email)
   

def bs_test(request):


    return render(request, "base.html",{"username":"test"})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/login")
    else:
        logout(request)
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        # TODO: 1. /login로 접근하면 로그인 페이지를 통해 로그인이 되게 해주세요
        # TODO: 2. login 할 때 form을 활용해주세요
        form=LoginForm(request.POST)
        msg="가입되어 있지 않거나 로그인 정보가 잘못 되었습니다."
        if form.is_valid():
            username=form.cleaned_data.get("username")
            raw_password=form.cleaned_data.get("password")
            user=authenticate(username=username, password=raw_password)
            if user is not None:
                msg="로그인 성공"
                login(request, user)
                #return render(request,"login.html",{"form":form, "msg":msg})
                return HttpResponseRedirect("/")
            else:
                form=AuthenticationForm()
                return render(request, "login.html" , {"form":form})

    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    # TODO: 3. /logout url을 입력하면 로그아웃 후 / 경로로 이동시켜주세요
    logout(request)							
    return HttpResponseRedirect("/")


# TODO: 8. user 목록은 로그인 유저만 접근 가능하게 해주세요
def user_list_view(request):
    if request.user.is_authenticated is False:
    
        return HttpResponseRedirect("/login")
    else:
        page=int(request.GET.get('page',1))
        users=User.objects.all().order_by("-id")

    paginator=Paginator(users, 10)
    users=paginator.get_page(page)
    
    return render(request, "users.html", {"users": users})
