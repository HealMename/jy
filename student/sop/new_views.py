from django.shortcuts import render
from .models import *
import time
import math
import random
from django.db.models import F,Sum
import hashlib
import os
from django.conf import settings
from django.http import HttpResponseRedirect
from .forms import *
def show_order(request):
    user_id = request.session['user_id']
    user = Users.objects.get(pk=user_id)
    order = Order.objects.filter(order_user=user)
    return render(request, 'sops/show_order.html', {'order': order, 'user': user})


def receive(request, goods_id, goods_stock):
    user_id = request.session['user_id']
    user = Users.objects.get(pk=user_id)
    goods = Goods.objects.get(pk=goods_id)
    Order.objects.filter(goods_id=goods_id).delete()
    order = Order.objects.filter(order_user=user)
    if not Deal_goods.objects.filter(goods_id=goods_id).exists():
        Deal_goods.objects.create(goods_name=goods.goods_name,
                                  goods_user=user,
                                  goods_id=goods.goods_id,
                                  goods_price=goods.goods_price,
                                  goods_stock=goods_stock)
        return render(request, 'sops/show_order.html', {'order': order, 'user': user})
    else:
        return render(request, 'sops/show_order.html', {'order': order, 'user': user})


def admins(request):
    admin = Admins.objects.filter(water='收入').aggregate(Sum('detail'))
    admins = Admins.objects.filter(water='支出').aggregate(Sum('detail'))
    incomes = Admins.objects.all()

    return render(request, 'sops/admin.html', {'admin': admin['detail__sum'],
                                               'admins': admins['detail__sum'],
                                               'incomes': incomes})


def incomes(request):
    admin = Admins.objects.filter(water='收入').aggregate(Sum('detail'))
    admins = Admins.objects.filter(water='支出').aggregate(Sum('detail'))
    incomes = Admins.objects.filter(water='收入')
    return render(request, 'sops/admin.html', {'admin': admin['detail__sum'],
                                               'admins': admins['detail__sum'],
                                               'incomes': incomes})


def expend(request):
    admin = Admins.objects.filter(water='收入').aggregate(Sum('detail'))
    admins = Admins.objects.filter(water='支出').aggregate(Sum('detail'))
    incomes = Admins.objects.filter(water='支出')
    return render(request, 'sops/admin.html', {'admin': admin['detail__sum'],
                                               'admins': admins['detail__sum'],
                                               'incomes': incomes})


def returus(request, goods_id, goods_stock):
    user_id = request.session['user_id']
    goods = Goods.objects.get(pk=goods_id)
    user = Users.objects.get(pk=user_id)
    order = Order.objects.all()
    Goods.objects.filter(pk=goods_id).update(goods_stock=F('goods_stock')+goods_stock)
    Users.objects.filter(pk=user_id).update(user_RMB=F('user_RMB')+(int(goods_stock)*int(goods.goods_price)))
    Order.objects.filter(goods_id=goods_id).delete()
    return render(request, 'sops/show_order.html', {'user': user, 'order': order})


def admin_time(request):
    admin = Admins.objects.filter(water='收入').aggregate(Sum('detail'))
    admins = Admins.objects.filter(water='支出').aggregate(Sum('detail'))
    incomes = Admins.objects.filter(times__month=request.POST['month'])
    return render(request, 'sops/admin.html', {'admin': admin['detail__sum'], 'admins': admins['detail__sum'], 'incomes': incomes})


def times(request):
    print(request.POST['times'])
    admin = Admins.objects.filter(water='收入').aggregate(Sum('detail'))
    admins = Admins.objects.filter(water='支出').aggregate(Sum('detail'))
    incomes = Admins.objects.all()
    return render(request, 'sops/admin.html', {'admin': admin['detail__sum'],
                                               'admins': admins['detail__sum'],
                                               'incomes': incomes})


def index(request):
    context = dict()

    if request.session.get('user_id'):
        user = Users.objects.get(pk=request.session['user_id'])
        context['user_id'] = user
        return render(request, 'sops/index.html', context)
    else:

        return render(request, 'sops/index.html')


def carter_user_img(img, user_id, ext):
    img_name = str(user_id) + ext

    img_path = os.path.join(settings.BASE_DIR, 'sop/static/user_head', img_name)
    print(img_path)
    with open(img_path, 'wb+') as a:
        for chunk in img.chunks():
            a.write(chunk)


def user_head(request):
    if request.session.get('user_id'):
        user_id = request.session['user_id']
        user = Users.objects.get(pk=user_id)
        imgs = request.FILES
        if len(imgs) > 0:
            print(imgs)
            ext = os.path.splitext(imgs['user_img'].name)[1]
            carter_user_img(imgs['user_img'], user_id, ext)
            img_name = 'user_head/'+str(user_id) + ext
            print(img_name)
            Users.objects.filter(pk=user_id).update(user_img=img_name)
            user = Users.objects.get(pk=user_id)
            return render(request, 'sops/user_xx.html', {'user_id': user})
        else:
            return render(request, 'sops/user_xx.html', {'user_id': user, 'succeed': '请选择一张图片'})
    return HttpResponseRedirect('/sop/')


def update_question(request):
    context = dict()
    form = UpdateQuestion()
    user = Users.objects.get(pk=request.session.get('user_id'))
    if request.method == 'POST':
        form = UpdateQuestion(request.POST)
        if form.is_valid():
            Users.objects.filter(pk=user.id).update(user_question=request.POST['question'],
                                                    user_answer=request.POST['answer'])
            context['succeed'] = '修改成功'
    context['form'] = form
    context['user_id'] = user
    return render(request, 'sops/update_question.html', context)


def update_goods(request, goods_id):
    context = dict()
    form = UpdateGoods()
    user = Users.objects.get(pk=request.session['user_id'])
    goods = Goods.objects.get(pk=goods_id)
    context['goods'] = goods
    context['user_id'] = user

    if request.method == 'POST':
        form = UpdateGoods(request.POST)
        if form.is_valid():
            Goods.objects.filter(pk=goods_id).update(
                goods_name=request.POST['goods_name'],
                goods_price=request.POST['goods_price'],
                goods_stock=request.POST['goods_stock'],
                goods_class=request.POST['goods_class'],
                goods_update=timezone.now(),
            )

            Update.objects.create(goods_id=goods.goods_id,
                                  goods_text='我修改了' + goods.goods_name + '的信息',
                                  goods_user=user)
            goods = Goods.objects.get(pk=goods_id)
            context['succeed'] = '修改成功'
            context['goods'] = goods
            return render(request, 'sops/update_goods.html', context)
        else:

            context['form'] = form
            return render(request, 'sops/update_goods.html', context)
    else:

        context['form'] = form

        return render(request, 'sops/update_goods.html', context)


def new_shop(request, goods_id):
    user = request.session.get('user_id')
    if user:
        cart = Carts.objects.filter(id=goods_id)




