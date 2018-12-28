from django import forms

from user.models import User


class Registerform(forms.Form):
    user_name = forms.CharField(max_length=20, required=True,
                            error_messages={
                                'required': '用户名是必填项',
                                'max_length': '用户名不能超过20个字'
                            })
    pwd = forms.CharField(min_length=5, max_length=20, required=True,
                               error_messages={
                                   'required': '密码是必填项',
                                   'max_length': '密码不能超过20位',
                                   'min_length': '密码不能少于5位'
                               })
    cpwd = forms.CharField(min_length=5, max_length=20, required=True,
                               error_messages={
                                   'required': '密码是必填项',
                                   'max_length': '密码不能超过20位',
                                   'min_length': '密码不能少于5位'
                               })

    email = forms.CharField(max_length=20, required=True,
                               error_messages={
                                   'required': '邮箱是必填项',
                                   'max_length': '邮箱不能超过20位'
                               })

    # 验证时会自动调用
    def clean(self):
        # 校验用户名是否已存在数据库
        user = User.objects.filter(username=self.cleaned_data.get('user_name'))
        if user:
            # 用户已存在数据库，抛出异常
            raise forms.ValidationError({'user_name': '该用户已存在，请直接登录！'})
        # 校验密码是否相等
        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        if pwd != cpwd:
            raise forms.ValidationError({'pwd': '两次密码不一致！'})


        return self.cleaned_data


class Loginform(forms.Form):
    username = forms.CharField(min_length=3, max_length=20, required=True,
                            error_messages={
                                'required': '用户名必填',
                                'max_length': '用户名不能超过20个字',
                                'min_length': '用户名不能少于3 位'
                            })
    pwd = forms.CharField(min_length=8, max_length=20, required=True,
                               error_messages={
                                   'required': '密码必填',
                                   'max_length': '密码不能超过20位',
                                   'min_length': '密码不能少于8位'
                               })

    def clean(self):
        # 验证登陆的账户是否已经注册过
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError({'username': '账号不存在，请先注册！'})

        return self.cleaned_data
