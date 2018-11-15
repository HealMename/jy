from django import forms
from .models import *


class Register(forms.ModelForm):
    accounts = dict(max_length='账号不能超过六位', required='账号不能为空', min_length='账号不能少于三位')
    names = dict(max_length='昵称不能超过十位', required='昵称不能为空', min_length='昵称不能少于三位')
    pas = dict(max_length='你的密码太长了', required='密码不能为空', min_length='你的密码太短了')
    co = dict(max_length='验证码错误', required='验证码不能为空', min_length='验证码错误')
    user_name = forms.CharField(max_length=10,
                                required=True,
                                min_length=3
                                , error_messages=names)
    user_account = forms.CharField(max_length=6,
                                   required=True,
                                   min_length=3,
                                   error_messages=accounts)
    user_password = forms.CharField(max_length=50,
                                    required=True,min_length=2,
                                    widget=forms.PasswordInput(),
                                    error_messages=pas)

    class Meta:
        model = Users
        fields = ['user_name', 'user_account', 'user_password']


class UserImg(forms.Form):
    user_img = forms.ImageField(label='更换头像', required=True)


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
    loser = dict(max_value='单次充值不得超过一万',
                 min_value='单次充值不得少于一',
                 required='请输入要充值的金额')
    user_RMB = forms.DecimalField(max_value=10000,
                                  min_value=1,
                                  label='请输入要充值的金额',
                                  required=True, error_messages=loser)


class Add_goods(forms.Form):
    goods_m = dict(max_length='商品名称太长了！',
                   min_length='商品名称太短了！',
                   required='商品名称不能为空')
    goods_p = dict(max_length='商品库存太多了！',
                   min_length='商品库存少了！',
                   required='商品库存不能为空')
    goods_s = dict(max_value='商品价格高了！',
                   min_value='商品价格太低了！！',
                   required='商品价格不能为空')
    goods_i = dict(required='请选择一张商品图片')
    goods_name = forms.CharField(max_length=50,
                                 min_length=1,
                                 label='商品名称',
                                 required=True, error_messages=goods_m)
    goods_price = forms.DecimalField(min_value=1,
                                     max_value=10000,
                                     label='商品价格',
                                     required=True, error_messages=goods_p)
    goods_stock = forms.DecimalField(max_value=1000,
                                     min_value=1,
                                     required=True,
                                     label='商品库存', error_messages=goods_s)
    goods_img = forms.ImageField(required=True, error_messages=goods_i)


class Carts(forms.Form):
    rmb = forms.DecimalField(max_value=10000, min_value=1, required=True)


class UpdateQuestion(forms.Form):
    question = forms.CharField(widget=forms.Select(choices=(('', '请选择你的密保问题'), ('你父母的姓名', '你父母的姓名'), ('你的名字', '你的名字'), ('你的手机号', '你的手机号'),)),
                               required=True,
                               label='')
    answer = forms.CharField(max_length=50,
                             min_length=1,
                             required=True,
                             label='密保答案')


class UpdateGoods(forms.Form):
    goods_na = dict(max_length='商品名称太长',
                    min_length='商品名称太短',
                    required='商品名称不能为空')
    goods_pr = dict(max_length='商品单价太大',
                    min_length='商品单价太小',
                    required='商品单价不能为空')
    goods_st = dict(max_length='商品库存太大',
                    min_length='商品名称太小',
                    required='商品库存不能为空')
    goods_name = forms.CharField(max_length=20,
                                 min_length=1,
                                 required=True,
                                 label='商品名称', error_messages=goods_na)
    goods_price = forms.DecimalField(max_value=10000,
                                     min_value=1,
                                     required=True,
                                     label='商品单价', error_messages=goods_pr)
    goods_stock = forms.IntegerField(max_value=10000,
                                     min_value=1,
                                     required=True,
                                     label='商品库存', error_messages=goods_st)


class Indent(forms.Form):
    goods_x = forms.IntegerField(max_value=20,
                                 min_value=1,
                                 required=True, label='购买数量')
    user_home = forms.CharField(max_length=200,
                                min_length=1,
                                required=True, label='收货地址')
    user_name = forms.CharField(max_length=5,
                                min_length=1,
                                required=True, label='收货人姓名')
    user_phone = forms.CharField(widget=forms.NumberInput(),
                                 max_length=13,
                                 min_length=7,
                                 required=True, label='联系电话')


class GoodsLyric(forms.Form):
    goods_details = forms.CharField(widget=forms.Textarea(),
                                    max_length=500,
                                    min_length=10,
                                    required=True,
                                    label='商品描述',
                                    )
    goods_lyric = forms.CharField(widget=forms.Textarea(), max_length=500,
                                  min_length=10,
                                  required=True, label='歌词')