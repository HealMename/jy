from django.shortcuts import render, reverse
from django.db.models import F, Sum

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
    user = Users.objects.get(pk=3)
    goods = Goods.objects.filter(goods_user=user)
    context['goods'] = goods
    print(goods)
    if request.session.get('user_id'):
        user = Users.objects.get(pk=request.session['user_id'])
        context['user_id'] = user
        return render(request, 'sops/index.html', context)
    else:

        return render(request, 'sops/index.html', context)


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


def show_book(request):
    context = dict()
    if request.session.get('user_id'):
        user_id = request.session['user_id']
        user = Users.objects.get(pk=user_id)
        user_bill = User_bill.objects.filter(user_name=user)
        context['user_id'] = user
        if user_bill:
            expend = User_bill.objects.filter(water='支出').filter(user_name=user)
            income = User_bill.objects.filter(water='收入').filter(user_name=user)
            expend_sum = expend.aggregate(Sum('detail'))['detail__sum']
            income_sum = income.aggregate(Sum('detail'))['detail__sum']
            context['expend'] = expend
            context['income'] = income
            context['expend_sum'] = expend_sum
            context['income_sum'] = income_sum
            context['profit'] = income_sum - expend_sum
        else:
            context['succeed'] = '您还没有账本！快去购买商品把！'

    return render(request, 'sops/show_book.html', context)


def indent(request, goods_id):
    context = dict()
    user_id = request.session.get('user_id', None)
    goods = Goods.objects.get(pk=goods_id)
    goods_de = GoodsDetails.objects.filter(goods=goods)
    context['goods'] = goods
    if user_id:
        user = Users.objects.get(pk=user_id)
        context['user_id'] = user
        if goods_de:
            context['goods_de'] = goods_de[0]
            print(goods_de)
        return render(request, 'sops/indent.html', context)
    return render(request, 'sops/indent.html', context)


def indent_s(request, goods_id):
    user_id = request.session.get('user_id', None)
    context = dict()
    form = Indent()
    if user_id:
        user = Users.objects.get(pk=user_id)
        goods = Goods.objects.get(pk=goods_id)
        context['user_id'] = user
        context['form'] = form
        context['goods'] = goods

        if request.method == 'POST':
            goods_x = int(request.POST['goods_x'])
            user_home = request.POST['user_home']
            user_phone = request.POST['user_phone']
            rmb = goods_x * int(goods.goods_price)
            print(rmb)
            print(user.user_RMB)
            if int(user.user_RMB) > int(rmb):
                if goods.goods_stock > goods_x:
                    Goods.objects.filter(pk=goods_id).update(goods_stock=F('goods_stock')-goods_x)
                    Users.objects.filter(pk=user_id).update(user_RMB=F('user_RMB') - rmb)
                    print(goods)
                    seller = Users.objects.get(goods=goods)
                    User_bill.objects.create(water='收入',
                                             detail=rmb,
                                             user_name=seller)
                    User_bill.objects.create(water='支出',
                                             detail=rmb,
                                             user_name=user)
                    Deal_goods.objects.create(goods_name=goods.goods_name,
                                              goods_user=user,
                                              goods_id=goods.goods_id,
                                              goods_price=goods.goods_price,
                                              goods_stock=goods.goods_stock)
                    context['user_id'] = Users.objects.get(pk=user_id)
                    context['goods'] = Goods.objects.get(pk=goods_id)
                    context['succeed'] = '添加成功'
                    if not Order.objects.filter(goods_id=goods_id).exists():
                        Order.objects.create(goods_id=goods_id,
                                             goods_name=goods.goods_name,
                                             goods_stock=goods_x,
                                             goods_address=goods.goods_address,
                                             user_home=user_home,
                                             order_user=user,
                                             user_phone=user_phone)
                    else:
                        Order.objects.filter(goods_id=goods_id).update(goods_stock=F('goods_stock')+goods_x)

                else:
                    context['succeed'] = '库存不足'
            else:
                context['succeed'] = '余额不足'
        return render(request, 'sops/indent_s.html', context)

    return HttpResponseRedirect(reverse('sop:index'))


def deposit(request):
    context = dict()
    form = Carts()
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(pk=user_id)
        context['user_id'] = user
        if request.method == 'POST':
            form = Carts(request.POST)
            Admins.objects.create(water='支出', detail=request.POST['rmb'])
            Users.objects.filter(pk=user_id).update(user_RMB=F('user_RMB')-request.POST['rmb'])
            context['succeed'] = '提现成功！预计两到三天到账！'
            context['form'] = form
        else:
            context['form'] = form
        return render(request, 'sops/deposit.html', context)


def goods_lyric(request, goods_id):
    context = dict()
    form = GoodsLyric()
    goods = Goods.objects.get(pk=goods_id)
    context['goods'] =goods
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(pk=user_id)
        context['user_id'] = user
        if request.method == 'POST':
            form = GoodsLyric(request.POST)
            if form.is_valid():
                dicts = dict(goods_details=request.POST['goods_details'], goods_lyric=request.POST['goods_lyric'])
                goods_details = GoodsDetails.objects.update_or_create(goods=goods, defaults=dicts
                                                                      )
                context['forms'] = form
                context['goods_de'] = goods_details
        context['forms'] = form
        return render(request, 'sops/update_goods.html', context)
    return HttpResponseRedirect(reverse('sop:home'))








