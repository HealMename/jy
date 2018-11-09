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
    return render(request, 'sops/admin.html', {'admin': admin['detail__sum'],
                                                   'admins': admins['detail__sum'],
                                                   'incomes': incomes})


def times(request):
    print(request.POST['times'])
    admin = Admins.objects.filter(water='收入').aggregate(Sum('detail'))
    admins = Admins.objects.filter(water='支出').aggregate(Sum('detail'))
    incomes = Admins.objects.all()
    return render(request, 'sops/admin.html', {'admin': admin['detail__sum'],
                                               'admins': admins['detail__sum'],
                                               'incomes': incomes})


def index(request):
    if request.session.get('user_id'):
        user = Users.objects.get(pk=request.session['user_id'])
        return render(request, 'sops/index.html', {'user_id': user})
    else:
        return render(request, 'sops/index.html')








