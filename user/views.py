from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from user.Userform import Registerform, Loginform
from user.models import User


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        form = Registerform(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['pwd']
            email = form.cleaned_data['email']
            new_password = make_password(password)
            User.objects.create(username=username, password=new_password, email=email)
            # 注意render和redirect的区别
            return HttpResponseRedirect(reverse('user:login'))
        else:
          return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        form = Loginform(request.POST)
        if form.is_valid():
            # 验证字段成功，验证了登录用户名已经存在数据库
            username = form.cleaned_data['username']
            pwd = form.cleaned_data['pwd']
            user = User.objects.filter(username=username).first()
            # 校验密码是否一致，一致返回True，不一致返回False
            if check_password(pwd, user.password):
                # 校验成功
                request.session['user_id'] = user.id

                return HttpResponseRedirect(reverse('goods:index'))
            else:
                # 密码错误
                err_pwd = '密码或者账号错误'
                return render(request, 'login.html', {'err_pwd': err_pwd})
        else:
            errors = form.errors
            return render(request, 'login.html', {'errors': errors})


def user_center_info(request):
    if request.method == 'GET':
        return render(request, 'user_center_info.html')


def user_center_site(request):
    if request.method == 'GET':
        return render(request, 'user_center_site.html')


def user_center_order(request):
    if request.method == 'GET':
        return render(request, 'user_center_order.html')