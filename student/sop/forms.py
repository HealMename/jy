from django import forms


class Register(forms.Form):
    accounts = dict(max_length='账号不能超过六位', required='账号不能为空', min_length='账号不能少于三位')
    names = dict(max_length='昵称不能超过十位', required='昵称不能为空', min_length='昵称不能少于三位')
    pas = dict(max_length='你的密码太长了', required='密码不能为空', min_length='你的密码太短了')
    co = dict(max_length='验证码错误', required='验证码不能为空', min_length='验证码错误')
    name = forms.CharField(max_length=10,
                           required=True,
                           min_length=3,
                           label='昵称', help_text='3~10', error_messages=names)
    account = forms.CharField(max_length=6,
                              required=True,
                              min_length=3,
                              label='账号', help_text='3~6', error_messages=accounts)
    passwords = forms.CharField(max_length=50,
                                required=True,
                                min_length=2,
                                label='密码',
                                widget=forms.PasswordInput(), help_text='3~6', error_messages=pas)
    code = forms.CharField(max_length=5,
                           required=True,
                           min_length=4,
                           label='验证', error_messages=co)


class Login(forms.Form):
    accounts = dict(max_length='账号不能超过六位', required='账号不能为空', min_length='账号不能少于三位')
    pas = dict(max_length='密码错误', required='密码不能为空', min_length='密码错误')
    co = dict(max_length='验证码错误', required='验证码不能为空', min_length='验证码错误')
    account = forms.CharField(max_length=6,
                              required=True,
                              min_length=3,
                              label='账号', error_messages=accounts
                              )
    password = forms.CharField(max_length=20,
                               required=True,
                               min_length=2,
                               label='密码',
                               widget=forms.PasswordInput(), error_messages=pas,
                               )
    code = forms.CharField(max_length=5,
                           required=True,
                           min_length=4,error_messages=co,
                           label='验证')


class Yue(forms.Form):
    rmb = forms.DecimalField(max_value=1000000,
                             min_value=1,
                             label='请输入要充值的金额',
                             required=True)


class Add_goods(forms.Form):
    name = forms.CharField(max_length=10,
                           min_length=1,
                           label='商品名称',
                           required=True)
    price = forms.DecimalField(min_value=1,
                               max_value=10000,
                               label='商品价格',
                               required=True)
    stock = forms.DecimalField(max_value=1000,
                               min_value=1,
                               required=True,
                               label='商品库存')


class Carts(forms.Form):
    stock = forms.DecimalField(max_value=1000,
                               min_value=1,
                               required=True,
                               label='购买数量')
